from copy import deepcopy

import numpy as np
from scipy.spatial.transform import Rotation as R
from shapely.geometry import box

from cap.envs.ur5_env_config import MAX_OBJ_RADIUS
from cap.helpers import logger


class LMP_wrapper():
    """Wrapper around an openai gym env.
    This wrapper provides utility methods for the LMP to call.
    """

    def __init__(self, env, cfg, render=False):
        self.env = env
        self._cfg = cfg
        self.object_names = list(self._cfg['env']['init_objs'])

        self._min_xy = np.array(self._cfg['env']['coords']['bottom_left'])
        self._max_xy = np.array(self._cfg['env']['coords']['top_right'])
        self._range_xy = self._max_xy - self._min_xy

        self._table_z = self._cfg['env']['coords']['table_z']
        self.render = render

    def is_obj_visible(self, obj_name):
        return obj_name in self.object_names

    def get_obj_names(self):
        return self.object_names[::]

    def denormalize_xy(self, pos_normalized):
        return pos_normalized * self._range_xy + self._min_xy

    def get_corner_positions(self):
        unit_square = box(0, 0, 1, 1)
        normalized_corners = np.array(list(unit_square.exterior.coords))[:4]
        corners = np.array(([self.denormalize_xy(corner) for corner in normalized_corners]))
        return corners

    def get_side_positions(self):
        side_xs = np.array([0, 0.5, 0.5, 1])
        side_ys = np.array([0.5, 0, 1, 0.5])
        normalized_side_positions = np.c_[side_xs, side_ys]
        side_positions = np.array(([self.denormalize_xy(corner) for corner in normalized_side_positions]))
        return side_positions

    def get_obj_pose(self, obj_name, request_callback=None):
        return self.env.get_obj_pose(obj_name, request_callback)

    def pick(self, pose):
        self.env.pick(pose)

    def place(self, pose):
        self.env.place(pose)

    def get_obj_pos(self, obj_name, request_callback=None):
        # return the xy position of the object in robot base frame
        # return self.env.get_obj_pos(obj_name)[0]
        return self.env.get_obj_pos(obj_name, request_callback)

    def get_obj_position_np(self, obj_name):
        return self.get_pos(obj_name)

    def get_bbox(self, obj_name):
        # return the axis-aligned object bounding box in robot base frame (not in pixels)
        # the format is (min_x, min_y, max_x, max_y)
        bbox = self.env.get_bounding_box(obj_name)
        return bbox

    def get_color(self, obj_name):
        return self.env.get_color(obj_name)

    def pick_place(self, pick_pos, place_pos):
        pick_pos_xyz = np.r_[pick_pos, [self._table_z]]
        place_pos_xyz = np.r_[place_pos, [self._table_z]]
        pass

    def put_first_on_second(self, arg1, arg2):
        # put the object with obj_name on top of target
        # target can either be another object name, or it can be an x-y position in robot base frame

        buffers = {}

        def request_callback(img, img_idx: int, buffers: dict):
            import cv2
            assert img_idx in [0, 1]
            success, buffer = cv2.imencode('.png', img)
            print('running request callback!')
            buffers[f'image{img_idx + 1}'] = buffer.tobytes()
            # files = {'image1': , 'image2': buffer.tobytes()}
            print('buffer', buffers.keys())

            # Send request once both keys are filled.
            if 'image1' in buffers and 'image2' in buffers:
                import os
                print('>>>>>>>>>>>>> sending the request!!')
                server_url = 'http://localhost:5000'
                import time
                started = time.time()
                import requests
                try:
                    response = requests.post(os.path.join(server_url, 'perception_image'), files=buffers)
                    print(response)
                except Exception as e:
                    import traceback
                    print('request failed')
                    traceback.print_exc()

        logger.info(f"=== Running put_first_on_second({arg1}, {arg2})")

        # Takuma: This is the only change necessary
        import functools
        pick_xy, pick_minz, pick_maxz, pick_axes = self.env.get_obj_pose(arg1, request_callback=functools.partial(request_callback, img_idx=0, buffers=buffers))
        # pick_xy, pick_minz, pick_maxz, pick_axes = self.env.get_obj_pos(arg1)

        pick_axis = pick_axes[1]

        # TODO: axis is the 2nd principal axis; its norm is the std_dev (in meters), which may be helpful for determining whether the estimation is valid or not
        pick_z = pick_maxz - self.env.pick_margin_ratio * (pick_maxz - pick_minz)
        pick_xyz = np.append(pick_xy, pick_z)

        if isinstance(arg2, str):
            place_xy, _, place_maxz, place_axes = self.env.get_obj_pose(arg2, request_callback=functools.partial(request_callback, img_idx=1, buffers=buffers)) if isinstance(arg2, str) else arg2
            # place_xy, _, place_maxz, place_axes = self.env.get_obj_pose(arg2, radius=np.linalg.norm(pick_axes[0]) * 3)
            place_axis = place_axes[1]
            place_z = (pick_z - pick_minz) + place_maxz
            if 'cup' not in arg1:
                place_z += self.env.place_margin
            place_xyz = np.append(place_xy, place_z)
        else:
            place_xyz = np.append(arg2, self.env.plane_z)
            place_axis = None

        # When axis is too large, it's likely a misdetection
        if np.linalg.norm(pick_axis) > MAX_OBJ_RADIUS:
            raise RuntimeError('Object segmentation (picking) seems wrong')
        if place_axis is not None and np.linalg.norm(place_axis) > MAX_OBJ_RADIUS:
            raise RuntimeError('Object segmentation (placing) seems wrong')

        qx, qy = pick_axis / np.linalg.norm(pick_axis)

        # Flip the vector to map to y > 0 space
        if qy < 0:
            qx = -qx
            qy = -qy

        rad = np.arctan2(qy, qx)  # -pi <= rad <= pi
        assert 0 <= rad <= np.pi

        delta_rad = rad  # How much should we rotate the gripper?
        if delta_rad > np.pi / 2:
            delta_rad = delta_rad - np.pi

        assert - np.pi / 2 < delta_rad <= np.pi / 2

        default_ori = self.env.arm.default_pose[-4:]
        place_ori = default_ori

        default_ori_rad = R.from_quat(default_ori).as_euler('xyz')
        target_ori_rad = deepcopy(default_ori_rad)
        target_ori_rad[2] = default_ori_rad[2] + delta_rad
        # print('default ori rad', default_ori_rad)
        # print('target ori rad', target_ori_rad)
        # print('=============================')
        pick_ori = R.from_euler('xyz', target_ori_rad).as_quat()

        pick_pose = np.array([*pick_xyz, *pick_ori])
        place_pose = np.array([*place_xyz, *place_ori])

        self.env.step(action={'pick': pick_pose, 'place': place_pose})
        # self.env.pick(pick_pose)
        # self.env.place(place_pose)

    def get_robot_pos(self):
        # return robot end-effector xy position in robot base frame
        return self.env.get_ee_pos()

    def goto_pos(self, position_xy):
        # move the robot end-effector to the desired xy position while maintaining same z
        ee_xyz = self.env.get_ee_pos()
        position_xyz = np.concatenate([position_xy, ee_xyz[-1]])
        while np.linalg.norm(position_xyz - ee_xyz) > 0.01:
            self.env.movep(position_xyz)
            self.env.step_sim_and_render()
            ee_xyz = self.env.get_ee_pos()

    def follow_traj(self, traj):
        for pos in traj:
            self.goto_pos(pos)

    def get_corner_positions(self):
        normalized_corners = np.array([
            [0, 1],
            [1, 1],
            [0, 0],
            [1, 0]
        ])
        return np.array(([self.denormalize_xy(corner) for corner in normalized_corners]))

    def get_side_positions(self):
        normalized_sides = np.array([
            [0.5, 1],
            [1, 0.5],
            [0.5, 0],
            [0, 0.5]
        ])
        return np.array(([self.denormalize_xy(side) for side in normalized_sides]))

    def get_corner_name(self, pos):
        corner_positions = self.get_corner_positions()
        corner_idx = np.argmin(np.linalg.norm(corner_positions - pos, axis=1))
        return ['top left corner', 'top right corner', 'bottom left corner', 'botom right corner'][corner_idx]

    def get_side_name(self, pos):
        side_positions = self.get_side_positions()
        side_idx = np.argmin(np.linalg.norm(side_positions - pos, axis=1))
        return ['top side', 'right side', 'bottom side', 'left side'][side_idx]

    def open_object(self, obj_name, pose):
        self.env.open_object(obj_name)

    def close_object(self, obj_name, pose):
        self.env.close_object(obj_name)

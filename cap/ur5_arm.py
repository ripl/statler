import base64
from copy import deepcopy
from typing import List

import cv2
import numpy as np
import roslibpy
from copy import deepcopy
from  cap.envs.ur5_env_config import ARM_LIMITS

from cap.envs.ur5_env_config import ENABLE_ROBOT, GRIPPER_CLOSE, GRIPPER_OPEN


def unpack_pos(rosmsg_pos):
    """Convert geometry_msgs/Point to a list"""
    x, y, z = rosmsg_pos['x'], rosmsg_pos['y'], rosmsg_pos['z']
    return [x, y, z]


def unpack_quat(rosmsg_quat):
    """Convert geometry_msgs/Quaternion to a list"""
    x, y, z, w = rosmsg_quat['x'], rosmsg_quat['y'], rosmsg_quat['z'], rosmsg_quat['w']
    return [x, y, z, w]


class UR5Arm:
    def __init__(self, default_pose=None) -> None:
        if default_pose is None:
            default_pose = [0.1, -0.4, 0.4, 0.928, -0.371, 0., 0.]
            # NOTE:
            # >>> r = R.from_quat([0.928, -0.371, 0., 0.])
            # >>> r.as_euler('xyz') * 180 / 3.141592
            # array([180.00003745,   0.        , -43.58153641])

        # bounding box of gripper
        self.limits = ARM_LIMITS

        # viewing position
        self.viewing_pos = [0.03, -0.32, 0.57]

        # self.target_state is formatted as xyz, quat, openess
        print('default pose', default_pose)
        self.default_pose = default_pose
        self.target_state = self.default_pose.copy()
        print('target_state', self.target_state)

        # rgbd image saved from subscribers
        self.image_dims = (480, 640, 3)
        self.rgb = np.zeros(self.image_dims, dtype=np.uint8)
        self.depth = np.zeros(self.image_dims[:2], dtype=np.uint16)

        # cam info and pose
        # self.cam_K = np.zeros((3, 3))  # intrinsic matrix
        self.cam_K = None
        self._store_caminfo = False

        # set up ros address
        # self.client = roslibpy.Ros(host='localhost', port=9090)
        self.client = roslibpy.Ros(host='bone.local', port=9090)
        self.client.run()
        print(f'connecting to rosbridge server...done -- is_connected: {self.client.is_connected}')

        # set up rgb + depth image services
        self.service_rgb = roslibpy.Service(self.client, '/image_srv/capture_image', 'capture_images/CaptureImage')
        self.request_rgb = roslibpy.ServiceRequest(values={'camera': {'data': 'arm_rgb'}})
        self.service_depth = roslibpy.Service(self.client, '/image_srv/capture_image', 'capture_images/CaptureImage')
        self.request_depth = roslibpy.ServiceRequest(values={'camera': {'data': 'arm_depth'}})

        # set up subscribers
        self.caminfo_subscriber = roslibpy.Topic(self.client, '/camera_arm/color/camera_info', 'sensor_msgs/CameraInfo')
        # self.camdepth_subscriber = roslibpy.Topic(self.client, '/camera_arm/depth/camera_info', 'sensor_msgs/CameraInfo')

        # start the subscribers
        self.caminfo_subscriber.subscribe(self.save_caminfo)
        # self.camdepth_subscriber.subscribe(self.save_caminfo)

        # Define a service client
        self.service_move = roslibpy.Service(self.client, '/external_control/execute_trajectory', 'ur5_cartesian_control/CartesianMoveTo')
        self.service_grasp = roslibpy.Service(self.client, '/external_control/grasp', 'ur5_cartesian_control/Grasp')
        self.service_tf = roslibpy.Service(self.client, '/external_control/lookup_tf', 'ur5_cartesian_control/LookupTransform')

    # check is a xyz position is in the bounding box
    def is_valid_pos(self, xyz):
        for i in range(3):
            if xyz[i] < self.limits[i, 0] or xyz[i] > self.limits[i, 1]:
                return False
        return True

    # save the intrinsic (K) of the cam
    def save_caminfo(self, message):
        if self._store_caminfo:
            self.cam_K = np.array(message['K']).reshape(3, 3)

    def get_caminfo(self):
        import time
        self._store_caminfo = True
        while self.cam_K is None:
            print('waiting for caminfo')
            time.sleep(0.5)
        self._store_caminfo = False
        return deepcopy(self.cam_K)

    # decode and reshape rgb images
    def get_rgb_image(self):
        print('calling the rgb service...')
        result = self.service_rgb.call(self.request_rgb)
        print('calling the rgb service...done')
        img = result['frame']

        base64_bytes = img['data'].encode('ascii')
        image_bytes = base64.b64decode(base64_bytes)
        np_arr = np.frombuffer(image_bytes, dtype=np.uint8)

        if img['encoding'] == 'rgb8':
            np_arr = np_arr.reshape((img['height'], img['width'], 3))
        else:
            raise NotImplementedError(f'Cannot deal with encoding {img["encoding"]} that is not "rgb8"')
        img = cv2.cvtColor(np_arr, cv2.COLOR_RGB2BGR)
        cv2.imwrite('rgb.png', img)
        self.rgb = np_arr
        return np_arr

    # decode and reshape depth images
    def get_depth_image(self):
        print('calling the depth service...')
        result = self.service_depth.call(self.request_depth)
        print('calling the detph service...done')
        img = result['frame']

        base64_bytes = img['data'].encode('ascii')
        image_bytes = base64.b64decode(base64_bytes)
        np_arr = np.frombuffer(image_bytes, dtype=np.uint16)

        if img['encoding'] == '16UC1':
            np_arr = np_arr.reshape((img['height'], img['width']))
            img = np_arr.copy()
            img[img > 1000] = 0
            normalized_img = (img - img.min()) / (img.max() - img.min())
            normalized_img = 255 * normalized_img
            # (Optional) crop propotion that is lost to aligning detph to color
            # np_arr = np_arr[:, 80:]
        else:
            raise NotImplementedError(f'Cannot deal with encoding {img["encoding"]} that is not "16UC1"')
        self.depth = np_arr / 1000  # mm -> m
        cv2.imwrite('depth.png', normalized_img)
        return np_arr

    def pose2request(self, target_pose: List[float]) -> dict:
        """
        target_pose: [x, y, z, qx, qy, qz, qw, grip]
        """
        x, y, z, qx, qy, qz, qw = target_pose
        request = roslibpy.ServiceRequest(
            values={
                'exec_time': 0,  # With this, server side computes the execution time based on traj length
                'target_pose': {'position': {'x': x, 'y': y, 'z': z},
                                'orientation': {'x': qx, 'y': qy, 'z': qz, 'w': qw}}
            }
        )
        return request

    def grip2request(self, grip: float) -> dict:
        return roslibpy.ServiceRequest(values={'grip': grip})

    def _move(self):
        """Move the arm and grasp"""
        pose = self.target_state

        # print('move target state', self.target_state)
        target_pose = self.pose2request([float(e) for e in pose])

        # print('Calling service...')
        if ENABLE_ROBOT:
            result = self.service_move.call(target_pose)
        else:
            result = {'success': True}
        # print('Service response: {}'.format(result))
        return result.get('success', False)

    def grasp(self, grip: float) -> bool:
        target_grasp = self.grip2request(grip)
        # print(f"Calling grasp service with {target_grasp}...")
        if ENABLE_ROBOT:
            result = self.service_grasp.call(target_grasp)
        else:
            result = {'success': True}
        # print(f"Calling grasp service with {target_grasp}...done")
        return result.get('success', False)

    def get_cam_pose(self):
        # get pose for the realsense camera

        request = roslibpy.ServiceRequest(
            values={
                'source_frame': {'data': '/camera_arm/camera_color_optical_frame'},
                'target_frame': {'data': '/ur_arm_base'}
            }
        )
        response = self.service_tf.call(request)
        trans = unpack_pos(response['transform']['position'])
        rot = unpack_quat(response['transform']['orientation'])
        # trans, rot = response['pose']['position'], response['pose']['orientation']
        cam_pose = np.array([*trans, *rot])

        cam_K = self.get_caminfo()
        return self.cam_K, cam_pose

    def get_rgbd(self):
        # move to the viewing position
        self.moveto_xyz(self.viewing_pos)

        # get rgbd output from the realsense camera
        rgb = self.get_rgb_image()
        depth = self.get_depth_image()
        depth = np.nan_to_num(self.depth, nan=2**10)
        return rgb.copy(), depth.copy()

    def moveto_xyz(self, pos):
        print(f'pos: {pos}')
        # move to a xyz position
        if self.is_valid_pos(pos):
            self.target_state[:3] = pos
            print(f'Moving to pos: {pos}...')
            self._move()
            print(f'Moving to pos: {pos}...DONE')
            return 1
        else:
            from cap.helpers.speaker import Speaker
            Speaker.say("The position is out of safe region")
            print(f'pos: {pos} is out of safe region!')
            return 0

    def moveto_pose(self, pose):
        pos = pose[:3]
        if self.is_valid_pos(pos):
            self.target_state = pose
            print(f'Moving to pose: {pose}...')
            self._move()
            print(f'Moving to pose: {pose}...DONE')
            return 1
        else:
            from cap.helpers.speaker import Speaker
            Speaker.say("The position is out of safe region")
            print(f'pos: {pos} is out of safe region!')
            return 0

    def close_grip(self):
        self.grasp(GRIPPER_CLOSE)

    def open_grip(self):
        self.grasp(GRIPPER_OPEN)

    def test_move_around_four_corners(self):
        """
        Move to all four corners with minimum z
        You can (physically) mark the corners on the table by running this.
        """
        min_z = ARM_LIMITS[2, 0]
        min_x, max_x = ARM_LIMITS[0, :]
        min_y, max_y = ARM_LIMITS[1, :]
        bottom_left = [max_x, max_y, min_z]
        top_left = [max_x, min_y, min_z]
        top_right = [min_x, min_y, min_z]
        bottom_right = [min_x, max_y, min_z]

        z_margin = 0.08

        for target_pos in [bottom_left, top_left, top_right, bottom_right]:
            self.moveto_xyz(self.default_pose[:3])
            _target_pos = deepcopy(target_pos)
            _target_pos[2] += z_margin
            self.moveto_xyz(_target_pos)
            input("Press enter to move to the next location")


if __name__ == '__main__':
    ur5 = UR5Arm()
    # while True:
    #     # import pdb; pdb.set_trace()
    #     img = cv2.cvtColor(ur5.rgbd[:, :, :3], cv2.COLOR_RGB2BGR)
    #     cv2.imwrite('output.png', img)
    #
    # ur5.get_cam_pose()
    ur5.test_move_around_four_corners()

    # result = ur5.moveto_xyz([0.1, -0.4, 0.3])
    # print('move to 1', result)
    # result = ur5.moveto_xyz([0.2, -0.4, 0.3])
    # print('move to 2', result)
    # result = ur5.moveto_xyz([0.2, -0.3, 0.3])
    # print('move to 3', result)

    # # import pdb; pdb.set_trace()
    # ur5.get_rgbd()

    # result = ur5.moveto_xyz([0.1, -0.4, 0.3])
    # print('move to 1', result)
    # result = ur5.moveto_xyz([0.2, -0.4, 0.3])
    # print('move to 2', result)
    # result = ur5.moveto_xyz([0.2, -0.3, 0.3])
    # print('move to 3', result)

    # try:
    #     while True:
    #         pass
    # except KeyboardInterrupt:
    #     ur5.client.terminate()

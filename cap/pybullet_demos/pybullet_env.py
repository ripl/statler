import os
import threading
from collections import defaultdict
from time import sleep
from typing import Tuple

import cv2
import numpy as np
import pybullet
import pybullet_data
import torch
import torch.nn.functional as F
import torchvision.transforms as T
from PIL import Image
from scipy.spatial.transform import Rotation
from skimage.color import rgb2lab
from sklearn.decomposition import PCA

from cap.pybullet_demos.pybullet_env_config import (BLOCK_SIZE, BOUNDS, COLORS_LAB, COLORS_RGB,
                                 CORNER_POS, DEBUG, LAB_TH, PIXEL_SIZE)
from cap.pybullet_demos.pybullet_env_config import (GRIPPER_CLOSE, PICK_MARGIN_RATIO,
                                PLACE_MARGIN, # PREGRASP_HEIGHT, PREPLACE_HEIGHT,
                                PREGRASP_MARGIN, PREPLACE_MARGIN)
from cap.helpers.utils import plot_results, rescale_bboxes

np.random.seed(0)

torch.set_grad_enabled(False)


# Gripper (Robotiq 2F85) code
class Robotiq2F85:
    """Gripper handling for Robotiq 2F85."""

    def __init__(self, robot, tool):
        self.robot = robot
        self.tool = tool
        pos = [0.1339999999999999, -0.49199999999872496, 0.5]
        rot = pybullet.getQuaternionFromEuler([np.pi, 0, np.pi])
        urdf = 'assets/robotiq_2f_85/robotiq_2f_85.urdf'
        self.body = pybullet.loadURDF(urdf, pos, rot)
        self.n_joints = pybullet.getNumJoints(self.body)
        self.activated = False
        self.default_pose = [
            0.13399591005559436,
            -0.49198216569019465,
            0.3306666536358444,
            4.156780714143499e-06,
            0.9999999994171225,
            3.3889174977042025e-05,
            1.4085775408768957e-10
        ]

        # Connect gripper base to robot tool.
        pybullet.createConstraint(self.robot, tool, self.body, 0, jointType=pybullet.JOINT_FIXED, jointAxis=[0, 0, 0], parentFramePosition=[0, 0, 0], childFramePosition=[0, 0, -0.07], childFrameOrientation=pybullet.getQuaternionFromEuler([0, 0, np.pi / 2]))

        # Set friction coefficients for gripper fingers.
        for i in range(pybullet.getNumJoints(self.body)):
            pybullet.changeDynamics(self.body, i, lateralFriction=10.0, spinningFriction=1.0, rollingFriction=1.0, frictionAnchor=True)

        # Start thread to handle additional gripper constraints.
        self.motor_joint = 1
        self.constraints_thread = threading.Thread(target=self.step)
        self.constraints_thread.daemon = True
        self.constraints_thread.start()

    # Control joint positions by enforcing hard contraints on gripper behavior.
    # Set one joint as the open/close motor joint (other joints should mimic).
    def step(self):
        while True:
            try:
                currj = [pybullet.getJointState(self.body, i)[0] for i in range(self.n_joints)]
                indj = [6, 3, 8, 5, 10]
                targj = [currj[1], -currj[1], -currj[1], currj[1], currj[1]]
                pybullet.setJointMotorControlArray(self.body, indj, pybullet.POSITION_CONTROL, targj, positionGains=np.ones(5))
            except BaseException:
                return
            sleep(0.001)

    # Close gripper fingers.
    def activate(self):
        pybullet.setJointMotorControl2(self.body, self.motor_joint, pybullet.VELOCITY_CONTROL, targetVelocity=1, force=10)
        self.activated = True

    # Open gripper fingers.
    def release(self):
        pybullet.setJointMotorControl2(self.body, self.motor_joint, pybullet.VELOCITY_CONTROL, targetVelocity=-1, force=10)
        self.activated = False

    # If activated and object in gripper: check object contact.
    # If activated and nothing in gripper: check gripper contact.
    # If released: check proximity to surface (disabled).
    def detect_contact(self):
        obj, _, ray_frac = self.check_proximity()
        if self.activated:
            empty = self.grasp_width() < 0.01
            cbody = self.body if empty else obj
            if obj == self.body or obj == 0:
                return False
            return self.external_contact(cbody)
    #   else:
    #     return ray_frac < 0.14 or self.external_contact()

    # Return if body is in contact with something other than gripper
    def external_contact(self, body=None):
        if body is None:
            body = self.body
        pts = pybullet.getContactPoints(bodyA=body)
        pts = [pt for pt in pts if pt[2] != self.body]
        return len(pts) > 0  # pylint: disable=g-explicit-length-test

    def check_grasp(self):
        while self.moving():
            sleep(0.001)
        success = self.grasp_width() > 0.01
        return success

    def grasp_width(self):
        lpad = np.array(pybullet.getLinkState(self.body, 4)[0])
        rpad = np.array(pybullet.getLinkState(self.body, 9)[0])
        dist = np.linalg.norm(lpad - rpad) - 0.047813
        return dist

    def check_proximity(self):
        ee_pos = np.array(pybullet.getLinkState(self.robot, self.tool)[0])
        tool_pos = np.array(pybullet.getLinkState(self.body, 0)[0])
        vec = (tool_pos - ee_pos) / np.linalg.norm((tool_pos - ee_pos))
        ee_targ = ee_pos + vec
        ray_data = pybullet.rayTest(ee_pos, ee_targ)[0]
        obj, link, ray_frac = ray_data[0], ray_data[1], ray_data[2]
        return obj, link, ray_frac

class PickPlaceEnv():
    def __init__(self, render=False, high_res=False, high_frame_rate=False, use_mdetr=False):
        self.dt = 1 / 480
        self.sim_step = 0

        # Configure and start PyBullet.
        # python3 -m pybullet_utils.runServer
        # pybullet.connect(pybullet.SHARED_MEMORY)  # pybullet.GUI for local GUI.
        pybullet.connect(pybullet.GUI)  # pybulletDIRECTfor local GUI.
        pybullet.configureDebugVisualizer(pybullet.COV_ENABLE_GUI, 0)
        pybullet.configureDebugVisualizer(pybullet.COV_ENABLE_SHADOWS, 0)
        pybullet.setPhysicsEngineParameter(enableFileCaching=0)
        assets_path = os.path.dirname(os.path.abspath(""))
        pybullet.setAdditionalSearchPath(assets_path)
        pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
        pybullet.setTimeStep(self.dt)

        self.home_joints = (np.pi / 2, -np.pi / 2, np.pi / 2, -np.pi / 2, 3 * np.pi / 2, 0)  # Joint angles: (J0, J1, J2, J3, J4, J5).
        self.home_ee_euler = (np.pi, 0, np.pi)  # (RX, RY, RZ) rotation in Euler angles.
        self.ee_link_id = 9  # Link ID of UR5 end effector.
        self.tip_link_id = 10  # Link ID of gripper finger tips.
        self.arm = None

        self.render = render
        self.high_res = high_res
        self.high_frame_rate = high_frame_rate

        # mdetr model
        self.use_mdetr = use_mdetr
        if self.use_mdetr:
            self.model_pc = torch.hub.load('ashkamath/mdetr:main', 'mdetr_efficientnetB3_phrasecut', pretrained=False, return_postprocessor=False)
            self.model_pc.load_state_dict(torch.load('mdetr_ckpts/phrasecut_EB3_checkpoint.pth')['model_ema'])
            self.model_pc = self.model_pc.cuda()
            self.model_pc.eval()

        # PCA
        self.pca = PCA()

        self.pick_margin = 0
        self.place_margin = 0
        self.plane_z = 0
        self.pick_margin_ratio = PICK_MARGIN_RATIO

    def reset(self, object_list):
        pybullet.resetSimulation(pybullet.RESET_USE_DEFORMABLE_WORLD)
        pybullet.setGravity(0, 0, -9.8)
        self.cache_video = []

        # Temporarily disable rendering to load URDFs faster.
        pybullet.configureDebugVisualizer(pybullet.COV_ENABLE_RENDERING, 0)

        # Add robot.
        pybullet.loadURDF("plane.urdf", [0, 0, -0.001])
        self.robot_id = pybullet.loadURDF("assets/ur5e/ur5e.urdf", [0, 0, 0], flags=pybullet.URDF_USE_MATERIAL_COLORS_FROM_MTL)
        self.ghost_id = pybullet.loadURDF("assets/ur5e/ur5e.urdf", [0, 0, -10])  # For forward kinematics.
        self.joint_ids = [pybullet.getJointInfo(self.robot_id, i) for i in range(pybullet.getNumJoints(self.robot_id))]
        self.joint_ids = [j[0] for j in self.joint_ids if j[2] == pybullet.JOINT_REVOLUTE]

        # Move robot to home configuration.
        for i in range(len(self.joint_ids)):
            pybullet.resetJointState(self.robot_id, self.joint_ids[i], self.home_joints[i])

        # Add gripper.
        if self.arm is not None:
            while self.arm.constraints_thread.is_alive():
                self.constraints_thread_active = False
        self.arm = Robotiq2F85(self.robot_id, self.ee_link_id)
        self.arm.release()

        # Add workspace.
        plane_shape = pybullet.createCollisionShape(pybullet.GEOM_BOX, halfExtents=[0.3, 0.3, 0.001])
        plane_visual = pybullet.createVisualShape(pybullet.GEOM_BOX, halfExtents=[0.3, 0.3, 0.001])
        plane_id = pybullet.createMultiBody(0, plane_shape, plane_visual, basePosition=[0, -0.5, 0])
        pybullet.changeVisualShape(plane_id, -1, rgbaColor=[0.8, 0.8, 0.8, 1.0])

        # Load objects according to config.
        self.object_list = object_list
        self.obj_name_to_id = {}
        obj_xyz = np.zeros((0, 3))

        # Add table
        if np.any(['table' in obj_name for obj_name in object_list]):
            self.obj_name_to_id['table'] = (plane_id,)
        else:
            self.obj_name_to_id['table'] = (plane_id,)
            print("Warning: no table in object list.")

        # Add disinfector
        if np.any(['disinfector' in obj_name for obj_name in object_list]):
            object_position = np.array([[-0.2, -0.3, 0.03]])
            object_id = pybullet.loadURDF("assets/bowl/wider_bowl.urdf")
            pybullet.resetBasePositionAndOrientation(object_id, object_position[0], [0, 0, -0.85, 0.85])
            pybullet.changeVisualShape(object_id, -1, rgbaColor=[1.0, 1.0, 1.0, 1.0])
            obj_xyz = np.concatenate((obj_xyz, object_position), axis=0)
            self.obj_name_to_id['disinfector'] = (object_id,)

        for obj_name in object_list:
            if ('block' in obj_name) or ('bowl' in obj_name):

                # Get random position 15cm+ from other objects.
                count = 0
                while True:
                    rand_x = np.random.uniform(BOUNDS[0, 0] + 0.1, BOUNDS[0, 1] - 0.1)
                    rand_y = np.random.uniform(BOUNDS[1, 0] + 0.1, BOUNDS[1, 1] - 0.1)
                    rand_xyz = np.float32([rand_x, rand_y, 0.03]).reshape(1, 3)
                    if len(obj_xyz) == 0:
                        obj_xyz = np.concatenate((obj_xyz, rand_xyz), axis=0)
                        break
                    else:
                        nn_dist = np.min(np.linalg.norm(obj_xyz - rand_xyz, axis=1)).squeeze()
                        if nn_dist > 0.12:
                            obj_xyz = np.concatenate((obj_xyz, rand_xyz), axis=0)
                            break

                    count += 1
                    if count > 1000:
                        raise RuntimeError("Could not find a valid position for object.")

                object_color = COLORS_RGB[obj_name.split(' ')[0]]
                object_type = obj_name.split(' ')[1]
                object_position = rand_xyz.squeeze()
                if object_type == 'block':
                    # orginal [0.2, 0.2, 0.2]
                    object_shape = pybullet.createCollisionShape(pybullet.GEOM_BOX, halfExtents=[0.015, 0.015, 0.015])
                    object_visual = pybullet.createVisualShape(pybullet.GEOM_BOX, halfExtents=[0.015, 0.015, 0.015])
                    object_id = pybullet.createMultiBody(0.01, object_shape, object_visual, basePosition=object_position)
                elif object_type == 'bowl':
                    object_position[2] = 0
                    # making the bowl wider so the gripper can pick blocks from it
                    object_id = pybullet.loadURDF("assets/bowl/wide_bowl.urdf", object_position, useFixedBase=1)

                # set the alpha value of clean objects to 1
                pybullet.changeVisualShape(object_id, -1, rgbaColor=np.array(object_color))
                self.obj_name_to_id[obj_name] = (object_id,)

        print('obj_xyz: ', obj_xyz)
        print('obj_name_to_id: ', self.obj_name_to_id)
        print('object_list: ', object_list)

        # Re-enable rendering.
        pybullet.configureDebugVisualizer(pybullet.COV_ENABLE_RENDERING, 1)

        for _ in range(200):
            pybullet.stepSimulation()

        # debug images
        cv2.imwrite('debug_top_down.png', cv2.cvtColor(self.get_observation()["image"], cv2.COLOR_BGR2RGB))
        cv2.imwrite('debug_camera.png', cv2.cvtColor(self.get_camera_image(), cv2.COLOR_BGR2RGB))

        # record object positions at reset
        self.init_pos = {name: self.get_obj_pos(name) for name in object_list}

        return self.get_observation()

    def servoj(self, joints):
        """Move to target joint positions with position control."""
        pybullet.setJointMotorControlArray(
            bodyIndex=self.robot_id,
            jointIndices=self.joint_ids,
            controlMode=pybullet.POSITION_CONTROL,
            targetPositions=joints,
            positionGains=[0.01] * 6)

    def movep(self, position):
        """Move to target end effector position."""
        joints = pybullet.calculateInverseKinematics(
            bodyUniqueId=self.robot_id,
            endEffectorLinkIndex=self.tip_link_id,
            targetPosition=position,
            targetOrientation=pybullet.getQuaternionFromEuler(self.home_ee_euler),
            maxNumIterations=100)
        self.servoj(joints)

    def get_ee_pos(self):
        ee_xyz = np.float32(pybullet.getLinkState(self.robot_id, self.tip_link_id)[0])
        return ee_xyz

    def get_ee_rot(self):
        # end effector rotation in quaternion
        ee_quat = np.float32(pybullet.getLinkState(self.robot_id, self.tip_link_id)[1])
        return ee_quat

    def move_to_target(self, target_xyz, max_steps=1000):
        # import pdb; pdb.set_trace()
        step = 0
        ee_xyz = self.get_ee_pos()
        while np.linalg.norm(target_xyz - ee_xyz) > 0.01:
            if step > max_steps:
                print('too many steps passed!')
                print('pos error:', np.linalg.norm(target_xyz - ee_xyz))
                return False
            self.movep(target_xyz)
            self.step_sim_and_render()
            ee_xyz = self.get_ee_pos()
            step += 1
        return True

    def noop(self, num_steps):
        for _ in range(num_steps):
            self.step_sim_and_render()

    def pick(self, pick_pos):
        # Now the format of pick_pos is always [x, y, z, quat]
        if pick_pos.shape == (7,):
            pick_xyz = pick_pos[:3]
            pick_xyz[2] = pick_xyz[2] + 0.015
        else:
            raise ValueError("Invalid pick_pos shape: {}".format(pick_pos.shape))

        default_xyz = np.float32([0, -0.5, 0.23])

        print(f"picking the object at {pick_xyz}")
        # Move to the default pos
        self.move_to_target(default_xyz)

        # Move to the object
        self.move_to_target(pick_xyz)

        # Grasp
        self.arm.activate()

        # Wait a bit (is this necessary?)
        self.noop(300)

        # Move to the default pos
        self.move_to_target(default_xyz)

        observation = self.get_observation()
        reward = self.get_reward()
        done = False
        info = {}
        return observation, reward, done, info

    def place(self, place_pos):
        # Now the format of place_pos is always [x, y, z, quat]
        if place_pos.shape == (7,):
            place_xyz = place_pos[:3]
        else:
            raise ValueError("Invalid place_pos shape: {}".format(place_pos.shape))

        default_xyz = np.float32([0, -0.5, 0.23])

        # Move to the position above the place pos
        target_xyz = place_xyz.copy()
        target_xyz[2] = 0.23
        self.move_to_target(target_xyz)

        z = self.get_highest_block_below(place_xyz[:2])
        place_xyz[2] = z

        # Place down the object
        self.move_to_target(place_xyz)

        self.noop(500)
        self.arm.release()

        # Wait a bit
        self.noop(240)

        # Move to the default location
        self.move_to_target(default_xyz)
        self.noop(50)
        observation = self.get_observation()
        reward = self.get_reward()
        done = False
        info = {}
        print("The final position", self.get_ee_pos())
        return observation, reward, done, info

    def get_highest_block_below(self, xy):
        block_heights = []
        bowl_under = False
        for obj in self.object_list:
            obj_xy = self.get_obj_pos(obj)[0]

            # append height if the block xy is close to the target xy
            if np.linalg.norm(obj_xy - xy) < 0.05:
                if 'bowl' in obj:
                    is_bowl = True
                if 'block' in obj:
                    block_heights.append(self.get_obj_pos(obj)[2])

        if len(block_heights) > 1:
            # return the second highest object + half of the size
            block_heights.sort()
            return block_heights[-2]
        elif bowl_under:
            return 0.04
        else:
            return 0.025

    def set_alpha_transparency(self, alpha: float) -> None:
        for id in range(20):
            visual_shape_data = pybullet.getVisualShapeData(id)
            for i in range(len(visual_shape_data)):
                object_id, link_index, _, _, _, _, _, rgba_color = visual_shape_data[i]
                rgba_color = list(rgba_color[0:3]) + [alpha]
                pybullet.changeVisualShape(
                    self.robot_id, linkIndex=i, rgbaColor=rgba_color)
                pybullet.changeVisualShape(
                    self.arm.body, linkIndex=i, rgbaColor=rgba_color)

    def step_sim_and_render(self):
        pybullet.stepSimulation()
        self.sim_step += 1

        interval = 40 if self.high_frame_rate else 120
        if self.sim_step % interval == 0 and self.render:
            self.cache_video.append(self.get_camera_image())

    def get_camera_image(self):
        if not self.high_res:
            image_size = (240, 240)
            intrinsics = (120., 0, 120., 0, 120., 120., 0, 0, 1)
        else:
            image_size = (1080, 1080)
            intrinsics = (540., 0, 540., 0, 540., 540., 0, 0, 1)
        color, _, _, _, _ = self.render_image(image_size, intrinsics)
        return color

    def get_reward(self):
        return None

    def get_observation(self):
        observation = {}

        # Render current image.
        color, depth, position, orientation, intrinsics = self.render_image()

        # Get heightmaps and colormaps.
        points = self.get_pointcloud(depth, intrinsics)
        position = np.float32(position).reshape(3, 1)
        rotation = pybullet.getMatrixFromQuaternion(orientation)
        rotation = np.float32(rotation).reshape(3, 3)
        transform = np.eye(4)
        transform[:3, :] = np.hstack((rotation, position))
        points = self.transform_pointcloud(points, transform)
        heightmap, colormap, xyzmap = self.get_heightmap(points, color, BOUNDS, PIXEL_SIZE)

        observation["image"] = colormap
        observation["xyzmap"] = xyzmap

        return observation

    def render_image(self, image_size=(720, 720), intrinsics=(360., 0, 360., 0, 360., 360., 0, 0, 1)):
        # Camera parameters.
        position = (0, -0.85, 0.4)
        orientation = (np.pi / 4 + np.pi / 48, np.pi, np.pi)
        orientation = pybullet.getQuaternionFromEuler(orientation)
        zrange = (0.01, 10.)
        noise = True

        # OpenGL camera settings.
        lookdir = np.float32([0, 0, 1]).reshape(3, 1)
        updir = np.float32([0, -1, 0]).reshape(3, 1)
        rotation = pybullet.getMatrixFromQuaternion(orientation)
        rotm = np.float32(rotation).reshape(3, 3)
        lookdir = (rotm @ lookdir).reshape(-1)
        updir = (rotm @ updir).reshape(-1)
        lookat = position + lookdir
        focal_len = intrinsics[0]
        znear, zfar = (0.01, 10.)
        viewm = pybullet.computeViewMatrix(position, lookat, updir)
        fovh = (image_size[0] / 2) / focal_len
        fovh = 180 * np.arctan(fovh) * 2 / np.pi

        # Notes: 1) FOV is vertical FOV 2) aspect must be float
        aspect_ratio = image_size[1] / image_size[0]
        projm = pybullet.computeProjectionMatrixFOV(fovh, aspect_ratio, znear, zfar)

        # Render with OpenGL camera settings.
        _, _, color, depth, segm = pybullet.getCameraImage(
            width=image_size[1],
            height=image_size[0],
            viewMatrix=viewm,
            projectionMatrix=projm,
            shadow=1,
            flags=pybullet.ER_SEGMENTATION_MASK_OBJECT_AND_LINKINDEX,
            renderer=pybullet.ER_BULLET_HARDWARE_OPENGL)

        # Get color image.
        color_image_size = (image_size[0], image_size[1], 4)
        color = np.array(color, dtype=np.uint8).reshape(color_image_size)
        color = color[:, :, :3]  # remove alpha channel
        if noise:
            color = np.int32(color)
            color += np.int32(np.random.normal(0, 3, color.shape))
            color = np.uint8(np.clip(color, 0, 255))

        # Get depth image.
        depth_image_size = (image_size[0], image_size[1])
        zbuffer = np.float32(depth).reshape(depth_image_size)
        depth = (zfar + znear - (2 * zbuffer - 1) * (zfar - znear))
        depth = (2 * znear * zfar) / depth
        if noise:
            depth += np.random.normal(0, 0.003, depth.shape)

        intrinsics = np.float32(intrinsics).reshape(3, 3)
        return color, depth, position, orientation, intrinsics

    def get_pointcloud(self, depth, intrinsics):
        """Get 3D pointcloud from perspective depth image.
        Args:
          depth: HxW float array of perspective depth in meters.
          intrinsics: 3x3 float array of camera intrinsics matrix.
        Returns:
          points: HxWx3 float array of 3D points in camera coordinates.
        """
        height, width = depth.shape
        xlin = np.linspace(0, width - 1, width)
        ylin = np.linspace(0, height - 1, height)
        px, py = np.meshgrid(xlin, ylin)
        px = (px - intrinsics[0, 2]) * (depth / intrinsics[0, 0])
        py = (py - intrinsics[1, 2]) * (depth / intrinsics[1, 1])
        points = np.float32([px, py, depth]).transpose(1, 2, 0)
        return points

    def transform_pointcloud(self, points, transform):
        """Apply rigid transformation to 3D pointcloud.
        Args:
          points: HxWx3 float array of 3D points in camera coordinates.
          transform: 4x4 float array representing a rigid transformation matrix.
        Returns:
          points: HxWx3 float array of transformed 3D points.
        """
        padding = ((0, 0), (0, 0), (0, 1))
        homogen_points = np.pad(points.copy(), padding,
                                'constant', constant_values=1)
        for i in range(3):
            points[Ellipsis, i] = np.sum(transform[i, :] * homogen_points, axis=-1)
        return points

    def get_heightmap(self, points, colors, bounds, pixel_size):
        """Get top-down (z-axis) orthographic heightmap image from 3D pointcloud.
        Args:
          points: HxWx3 float array of 3D points in world coordinates.
          colors: HxWx3 uint8 array of values in range 0-255 aligned with points.
          bounds: 3x2 float array of values (rows: X,Y,Z; columns: min,max) defining
            region in 3D space to generate heightmap in world coordinates.
          pixel_size: float defining size of each pixel in meters.
        Returns:
          heightmap: HxW float array of height (from lower z-bound) in meters.
          colormap: HxWx3 uint8 array of backprojected color aligned with heightmap.
          xyzmap: HxWx3 float array of XYZ points in world coordinates.
        """
        width = int(np.round((bounds[0, 1] - bounds[0, 0]) / pixel_size))
        height = int(np.round((bounds[1, 1] - bounds[1, 0]) / pixel_size))
        heightmap = np.zeros((height, width), dtype=np.float32)
        colormap = np.zeros((height, width, colors.shape[-1]), dtype=np.uint8)
        xyzmap = np.zeros((height, width, 3), dtype=np.float32)

        # Filter out 3D points that are outside of the predefined bounds.
        ix = (points[Ellipsis, 0] >= bounds[0, 0]) & (points[Ellipsis, 0] < bounds[0, 1])
        iy = (points[Ellipsis, 1] >= bounds[1, 0]) & (points[Ellipsis, 1] < bounds[1, 1])
        iz = (points[Ellipsis, 2] >= bounds[2, 0]) & (points[Ellipsis, 2] < bounds[2, 1])
        valid = ix & iy & iz
        points = points[valid]
        colors = colors[valid]

        # Sort 3D points by z-value, which works with array assignment to simulate
        # z-buffering for rendering the heightmap image.
        iz = np.argsort(points[:, -1])
        points, colors = points[iz], colors[iz]
        px = np.int32(np.floor((points[:, 0] - bounds[0, 0]) / pixel_size))
        py = np.int32(np.floor((points[:, 1] - bounds[1, 0]) / pixel_size))
        px = np.clip(px, 0, width - 1)
        py = np.clip(py, 0, height - 1)
        heightmap[py, px] = points[:, 2] - bounds[2, 0]
        for c in range(colors.shape[-1]):
            colormap[py, px, c] = colors[:, c]
            xyzmap[py, px, c] = points[:, c]
        colormap = colormap[::-1, :, :]  # Flip up-down.
        xv, yv = np.meshgrid(np.linspace(BOUNDS[0, 0], BOUNDS[0, 1], height),
                             np.linspace(BOUNDS[1, 0], BOUNDS[1, 1], width))
        xyzmap[:, :, 0] = xv
        xyzmap[:, :, 1] = yv
        xyzmap = xyzmap[::-1, :, :]  # Flip up-down.
        heightmap = heightmap[::-1, :]  # Flip up-down.
        return heightmap, colormap, xyzmap

    def on_top_of(self, obj_a, obj_b):
        """
        check if obj_a is on top of obj_b
        condition 1: l2 distance on xy plane is less than a threshold
        condition 2: obj_a is higher than obj_b
        """
        obj_a_pos = self.get_obj_pos(obj_a)
        obj_b_pos = self.get_obj_pos(obj_b)
        xy_dist = np.linalg.norm(obj_a_pos[:2] - obj_b_pos[:2])
        if obj_b in CORNER_POS:
            is_near = xy_dist < 0.06
            return is_near
        elif 'bowl' in obj_b:
            is_near = xy_dist < 0.06
            is_higher = obj_a_pos[2] > obj_b_pos[2]
            return is_near and is_higher
        else:
            is_near = xy_dist < 0.04
            is_higher = obj_a_pos[2] > obj_b_pos[2]
            return is_near and is_higher

    def get_obj_id(self, obj_name):
        try:
            if obj_name in self.obj_name_to_id:
                obj_id = self.obj_name_to_id[obj_name]
            else:
                obj_name = obj_name.replace('circle', 'bowl').replace('square', 'block').replace('small', '').strip()
                obj_id = self.obj_name_to_id[obj_name]
            return obj_id
        except BaseException:
            print(f'requested_name="{obj_name}"')
            print(f'available_objects_and_id="{self.obj_name_to_id}')
            exit(1)

    def get_text_mask(self, img_np, block_name):
        transform = T.Compose([
            T.Resize(800),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        img_pil = Image.fromarray(np.uint8(img_np))
        img_tensor = transform(img_pil).unsqueeze(0).cuda()

        # propagate through the model
        outputs = self.model_pc(img_tensor, [block_name])

        # keep only predictions with 0.9+ confidence
        probas = 1 - outputs['pred_logits'].softmax(-1)[0, :, -1].cpu()
        keep = (probas > 0.9).cpu()

        if DEBUG:
            img_pil.save('test_img.png')
            print('input text: ', block_name)
            print('number of keep: ', keep.sum())

        # Interpolate masks to the correct size
        w, h = img_pil.size
        masks = F.interpolate(outputs["pred_masks"], size=(h, w), mode="bilinear", align_corners=False)
        masks = masks.cpu()[0, keep].sigmoid() > 0.5

        if DEBUG:
            # convert boxes from [0; 1] to image scales
            bboxes_scaled = rescale_bboxes(outputs['pred_boxes'].cpu()[0, keep], img_pil.size)

            tokenized = self.model_pc.detr.transformer.tokenizer.batch_encode_plus([block_name], padding="longest", return_tensors="pt").to(img_tensor.device)

            # Extract the text spans predicted by each box
            positive_tokens = (outputs["pred_logits"].cpu()[0, keep].softmax(-1) > 0.1).nonzero().tolist()
            predicted_spans = defaultdict(str)
            for tok in positive_tokens:
                item, pos = tok
                if pos < 255:
                    span = tokenized.token_to_chars(0, pos)
                    predicted_spans[item] += " " + block_name[span.start:span.end]

            labels = [predicted_spans[k] for k in sorted(list(predicted_spans .keys()))]
            plot_results(img_pil, probas[keep], bboxes_scaled, labels, masks, block_name)

        masks = masks.squeeze(0)
        return masks

    def get_color_mask(self, img, color):
        '''
        Given
        1. rgb image of dimension Height x Width x 3
        2. query color as string
        return
        a per-pixel mask
        '''
        # img: HxWx3
        assert img.shape[-1] == 3
        if color in COLORS_LAB:
            color = COLORS_LAB[color]
        else:
            raise Exception("color not hardcoded ;-;")
        img_lab = rgb2lab(img)
        masks = np.linalg.norm((img_lab - color)[..., 1:], axis=-1) < LAB_TH

        return masks

    def get_block_center(self, block_info):
        '''
        Given:
        query block info (color or object name)
        return
        the center coordinate
        '''
        rgb, depth, position, orientation, intrinsics = self.render_image()
        points = self.get_pointcloud(depth, intrinsics)
        position = np.float32(position).reshape(3, 1)
        rotation = Rotation.from_quat(orientation).as_matrix()
        transform = np.eye(4)
        transform[:3, :] = np.hstack((rotation, position))
        points = self.transform_pointcloud(points, transform)

        if self.use_mdetr:
            mask = self.get_text_mask(rgb, block_info)
        else:
            mask = self.get_color_mask(rgb, block_info)

        block_coords = points[mask]
        center_coord = np.mean(block_coords, axis=0)
        dists = np.linalg.norm(block_coords - center_coord, axis=-1)
        block_coords = block_coords[dists < np.quantile(dists, 0.95)]
        center_coord = np.stack((block_coords.min(axis=0), block_coords.max(axis=0))).mean(axis=0)

        return center_coord

    def get_block_geometry(self, block_info, request_callback = None) -> Tuple[np.ndarray, float, float]:
        '''
        Given:
            - query block info (color or object name)
        Return:
            - xy coordinate of the center of the block
            - minimum z of the block
            - maximum z of the block
            - 2nd principal axis
        '''
        rgb, depth, position, orientation, intrinsics = self.render_image()
        points = self.get_pointcloud(depth, intrinsics)
        position = np.float32(position).reshape(3, 1)
        rotation = Rotation.from_quat(orientation).as_matrix()
        cam2base = np.eye(4)
        cam2base[:3, :] = np.hstack((rotation, position))
        points = self.transform_pointcloud(points, cam2base)

        if self.use_mdetr:
            mask = self.get_text_mask(rgb, block_info)
        else:
            mask = self.get_color_mask(rgb, block_info)
        # if DEBUG:
        #     mask, img_plt = mask

        block_coords = points[mask]
        center_coord = np.mean(block_coords, axis=0)
        dists = np.linalg.norm(block_coords - center_coord, axis=-1)
        block_coords = block_coords[dists < np.quantile(dists, 0.95)]
        self.pca.fit(block_coords[:, :2])
        axes = self.pca.components_ * np.sqrt(self.pca.explained_variance_)[:, None]

        # if DEBUG:
        #     pts = np.tile(center_coord, (3, 1))
        #     pts[1:, :2] += axes * 3
        #     uvs = pt2uv(pts, np.linalg.inv(cam2base), intrinsics)
        #     cv2.arrowedLine(img_plt, uvs[0], uvs[1], (255, 0, 0))
        #     cv2.arrowedLine(img_plt, uvs[0], uvs[2], (0, 255, 0))

        #     # block_info = block_info.replace(' ', '_')
        #     # fname = f'{block_info}__debug.png'
        #     # print('writing to', fname)
        #     # cv2.imwrite(fname, img_plt[..., ::-1])

        #     import time
        #     started = time.time()
        #     if request_callback is not None:
        #         request_callback(img_plt[..., ::-1])
        #     elapsed = time.time() - started
        #     print(f'posting image took {elapsed}')

        min_coords = block_coords.min(axis=0)
        max_coords = block_coords.max(axis=0)
        center_coord = np.stack((min_coords, max_coords)).mean(axis=0)

        return center_coord[:2], min_coords[2], max_coords[2], axes[1]

    def get_obj_pos_from_name(self, obj_name, request_callback = None) -> Tuple[np.ndarray, float, float]:
        # orientation is currently not implemented
        if self.use_mdetr:
            return self.get_block_geometry(obj_name, request_callback)
        color = ''
        for key in COLORS_LAB.keys():
            if key in obj_name:
                color = key
                break
        if not color:
            raise Exception(obj_name, 'color not hardcoded')
        return self.get_block_geometry(color)

    def get_obj_pos(self, obj_name, detect_not_query=False, request_callback = None):
        if isinstance(obj_name, list):
            obj_name = obj_name[0]

        obj_name = obj_name.replace('the', '').replace('_', ' ').strip()
        if obj_name in CORNER_POS:
            return np.float32(np.array(CORNER_POS[obj_name]))
        else:
            if detect_not_query:
                pose_info = self.get_obj_pos_from_name(obj_name, request_callback)
                return pose_info
            else:
                pick_id = self.get_obj_id(obj_name)
                if len(pick_id) == 1:
                    pose = pybullet.getBasePositionAndOrientation(pick_id[0])
                elif len(pick_id) == 2:
                    pose = pybullet.getLinkState(pick_id[0], pick_id[1])
                position = np.float32(pose[0])
                z = position[2]
                pca_2nd_axes = np.array([0.00532912, 0.00994585]) # dummy
                return position[:2], z - BLOCK_SIZE / 2, z + BLOCK_SIZE / 2, pca_2nd_axes

    def get_color(self, obj_name):
        for color, rgb in COLORS_RGB.items():
            if color in obj_name:
                return rgb

    def exit(self):
        pybullet.disconnect()
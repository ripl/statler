#!/usr/bin/env python3
import numpy as np
from sklearn.decomposition import PCA
from cap.envs.ur5_env_config import (ALL_BLOCKS, COLORS_LAB, CORNER_POS, DEBUG,
                            GRIPPER_CLOSE, LAB_TH, PICK_MARGIN_RATIO,
                            PLACE_MARGIN, # PREGRASP_HEIGHT, PREPLACE_HEIGHT,
                            PREGRASP_MARGIN, PREPLACE_MARGIN,
                            USE_ROS, ARM_LIMITS)
from cap.helpers import logger


class DummyArm:
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
        logger.info('default pose', default_pose)
        self.default_pose = default_pose
        self.target_state = self.default_pose.copy()
        logger.info('target_state', self.target_state)

        # rgbd image saved from subscribers
        self.image_dims = (480, 640, 3)
        self.rgb = np.zeros(self.image_dims, dtype=np.uint8)
        self.depth = np.zeros(self.image_dims[:2], dtype=np.uint16)

        self.cam_K = None
        self._store_caminfo = False


class DummyEnv:
    # Env class for UR5 that matches the lmp_wapper API
    def __init__(self, default_pos=None, use_mdetr=True) -> None:
        self.arm = DummyArm(default_pos)
        self.gripper_margin = 0.11
        self.pick_margin_ratio = PICK_MARGIN_RATIO
        self.place_margin = PLACE_MARGIN
        self.plane_z = self.arm.limits[2][0]
        self.object_list = ALL_BLOCKS
        self.use_mdetr = use_mdetr
        self.pca = PCA()

    def reset(self):
        logger.info('dummy - reset')

    def step(self, action):
        logger.info('dummy - executing action', action)

    def get_obj_pos(self, obj_name, radius=None, request_callback=None):
        """
        Returns
          - pick_xy
          - pick_minz
          - pick_maxz
          - axis (shape: (2,)): 2nd principal axis of PCA
        """
        logger.info('dummy - get_obj_pos', obj_name, radius)
        ret = np.float32(np.array(CORNER_POS['middle']))
        logger.info('dummy - get_obj_pos ret', ret)

        # Dummy values
        pick_xy = [0, 0]
        pick_minz = 0
        pick_maxz = 0.1
        axis = [[0.02, 0.02], [0.02, 0.02]]
        return pick_xy
    
    def get_obj_pose(self, obj_name, radius=None, request_callback=None):
        """
        Returns
          - pick_xy
          - pick_minz
          - pick_maxz
          - axis (shape: (2,)): 2nd principal axis of PCA
        """
        logger.info('dummy - get_obj_pos', obj_name, radius)
        ret = np.float32(np.array(CORNER_POS['middle']))
        logger.info('dummy - get_obj_pos ret', ret)

        # Dummy values
        pick_xy = [0, 0]
        pick_minz = 0
        pick_maxz = 0.1
        axis = [[0.02, 0.02], [0.02, 0.02]]
        return pick_xy, pick_minz, pick_maxz, axis
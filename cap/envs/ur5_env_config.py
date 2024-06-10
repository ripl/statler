import json

import numpy as np
from skimage.color import rgb2lab

from cap.helpers import rootdir

DEBUG = True

# use ros to debug
USE_ROS = False

# enable robot movement
ENABLE_ROBOT = True

# use mdetr to detect block or not
USE_MDETR = True

# # Global constants: pick and place objects, colors, workspace bounds
COLORS_RGB = {
    'red': (95 / 255, 25 / 255, 21 / 255, 255 / 255),
    'green': (42 / 255, 134 / 255, 83 / 255, 255 / 255),
    'blue': (0 / 255, 70 / 255, 102 / 255, 255 / 255),
    'yellow': (156 / 255, 135 / 255, 39 / 255, 255 / 255),
    'orange': (242 / 255, 142 / 255, 43 / 255, 255 / 255),
    'purple': (176 / 255, 122 / 255, 161 / 255, 255 / 255),
    'pink': (255 / 255, 157 / 255, 167 / 255, 255 / 255),
    'cyan': (118 / 255, 183 / 255, 178 / 255, 255 / 255),
    'brown': (156 / 255, 117 / 255, 95 / 255, 255 / 255),
    'gray': (186 / 255, 176 / 255, 172 / 255, 255 / 255),
}
COLORS_LAB = {key: rgb2lab(np.array(val[:3])) for key, val in COLORS_RGB.items()}
LAB_TH = 16


# TODO: Read the minimum z height (i.e., table height) from disk, and reflect it
# Use hand_finger_tip_link and ur_arm_base

tool0_to_fingertip = 0.091
with open(rootdir / 'table_corners.json', 'r') as f:
    table_corners = json.load(f)
min_z = np.mean([z for _, _, z in table_corners.values()])
# min_z += 0.27 + 0.01
min_z += tool0_to_fingertip


# Ranges of x, y, z
# NOTE: <-- x | y down
# ARM_LIMITS = np.array([[-0.34, 0.3], [-0.64, -0.2], [0.05, 0.57]])
ARM_LIMITS = np.array([[-0.34, 0.3], [-0.64, -0.2], [min_z, 0.57]])
min_z = ARM_LIMITS[2, 0]
min_x, max_x = ARM_LIMITS[0, :]
min_y, max_y = ARM_LIMITS[1, :]
bottom_left = [max_x, max_y, min_z]
top_left = [max_x, min_y, min_z]
top_right = [min_x, min_y, min_z]
bottom_right = [min_x, max_y, min_z]

CORNER_POS = {
    'top left corner': (-0.3 + 0.05, -0.2 - 0.05, 0),
    'top side': (0, -0.2 - 0.05, 0),
    'top right corner': (0.3 - 0.05, -0.2 - 0.05, 0),
    'left side': (-0.3 + 0.05, -0.5, 0),
    'middle': (0, -0.5, 0),
    'right side': (0.3 - 0.05, -0.5, 0),
    'bottom left corner': (-0.3 + 0.05, -0.8 + 0.05, 0),
    'bottom side': (0, -0.8 + 0.05, 0),
    'bottom right corner': (0.3 - 0.05, -0.8 + 0.05, 0),
}

# ALL_BLOCKS = ['red block', 'green block', 'blue block', 'yellow block']
ALL_BLOCKS = [
    # 'black plate',
    # 'bread toy',
    # 'brown circle',
    # 'brown stick',
    'butter toy',
    'bread loaf',
    # 'triangular cheese toy',
    'lemon',
    'orange',
    'pen',
    'Rubik\'s cube',
    'red tomato',
    'toy duckie',  # Or circular brown chocolate
    'white fish toy',
    'drawer',
    # 'garlic',
    'banana',
    'black tray',
    # 'black plate',
    'wooden drawer',
]

ALL_BOWLS = []

GRIPPER_CLOSE = 1.0
GRIPPER_OPEN = 0.17

PREGRASP_MARGIN = PREPLACE_MARGIN = 0.15

PICK_MARGIN_RATIO = 0.6
PLACE_MARGIN = 0.003

# Threshold to decide whether the object detection is wrong or not
MAX_OBJ_RADIUS = 0.1

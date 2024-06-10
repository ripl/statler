import numpy as np
from skimage.color import rgb2lab

DEBUG = False

# use mdetr to detect block or not
USE_MDETR = False

# # Global constants: pick and place objects, colors, workspace bounds
COLORS_RGB = {
    'gold': (255 / 255, 215 / 255, 0 / 255, 255 / 255),
    'tan': (210 / 255, 180 / 255, 140 / 255, 255 / 255),
    'platinum': (229 / 255, 228 / 255, 226 / 255, 255 / 255),
    'magenta': (255 / 255, 0 / 255, 255 / 255, 255 / 255),
    'rust': (183 / 255, 65 / 255, 14 / 255, 255 / 255),
    'plastic': (255 / 255, 255 / 255, 255 / 255, 125 / 255),
    'bronze': (205 / 255, 127 / 255, 50 / 255, 255 / 255),
    'golden': (255 / 255, 215 / 255, 0 / 255, 255 / 255),
    'silver': (192 / 255, 192 / 255, 192 / 255, 255 / 255),
    'black': (0 / 255, 0 / 255, 0 / 255, 255 / 255),
    'transparent': (255 / 255, 255 / 255, 255 / 255, 100 / 255),
    'white': (255 / 255, 255 / 255, 255 / 255, 255 / 255),
    'blue': (78 / 255, 121 / 255, 167 / 255, 255 / 255),
    'red': (255 / 255, 87 / 255, 89 / 255, 255 / 255),
    'green': (89 / 255, 169 / 255, 79 / 255, 255 / 255),
    'orange': (242 / 255, 142 / 255, 43 / 255, 255 / 255),
    'yellow': (237 / 255, 201 / 255, 72 / 255, 255 / 255),
    'purple': (176 / 255, 122 / 255, 161 / 255, 255 / 255),
    'pink': (255 / 255, 157 / 255, 167 / 255, 255 / 255),
    'cyan': (118 / 255, 183 / 255, 178 / 255, 255 / 255),
    'brown': (156 / 255, 117 / 255, 95 / 255, 255 / 255),
    'gray': (186 / 255, 176 / 255, 172 / 255, 255 / 255),
}
COLORS_LAB = {key: rgb2lab(np.array(val[:3])) for key, val in COLORS_RGB.items()}
LAB_TH = 10

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

BLOCK_SIZE = 0.06  # hardcoding block size

ALL_BLOCKS = ['blue block', 'red block', 'green block', 'orange block', 'yellow block', 'purple block', 'pink block', 'cyan block', 'brown block', 'gray block']
ALL_BOWLS = ['blue bowl', 'red bowl', 'green bowl', 'orange bowl', 'yellow bowl', 'purple bowl', 'pink bowl', 'cyan bowl', 'brown bowl', 'gray bowl']

PIXEL_SIZE = 0.00267857
BOUNDS = np.float32([[-0.3, 0.3], [-0.8, -0.2], [0, 0.15]])  # X Y Z

GRIPPER_CLOSE = 1.0
GRIPPER_OPEN = 0.17

PREGRASP_MARGIN = PREPLACE_MARGIN = 0.15

PICK_MARGIN_RATIO = 0.99
PLACE_MARGIN = 0.01

# Threshold to decide whether the object detection is wrong or not
MAX_OBJ_RADIUS = 0.1


# %% [markdown]
# # Interactive Tabletop Manipulation
#
# Instructions:
#
# 1. Set the number of blocks and bowls with the sliders in the next cell.
# 2. Input a command in the `user_input` field below and run the cell. This will run Code as Policies by querying the code-generating LLM to write robot code to complete the task.
#
# Note the object names printed after the Initilize Env cell - these are the objects in the scene and can be referred to in the commands.
#
# Supported commands:
# * Spatial reasoning (e.g. to the left of the red block, the closest corner, the farthest bowl, the second block from the right)
# * Sequential actions (e.g. put blocks in matching bowls, stack blocks on the bottom right corner)
# * Contextual commands (e.g. do the same with the blue block, undo that)
# * Language-based reasoning (e.g. put the forest-colored block on the ocean-colored bowl).
# * Simple Q&A (e.g. how many blocks are to the left of the blue bowl?)
#
# Example commands (note object names may need to be changed depending the sampled object names):
# * put the sun-colored block on the bowl closest to it
# * stack the blocks on the bottom most bowl
# * arrange the blocks as a square in the middle
# * move the square 5cm to the right
# * how many blocks are to the right of the orange bowl?
# * pick up the block closest to the top left corner and place it on the bottom right corner
#
# Known limitations:
# * In simulation we're using ground truth object poses instead of using vision models. This means that commands the require knowledge of visual apperances (e.g. darkest bowl, largest object) are not supported.
# * Currently, the low-level pick place primitive does not do collision checking, so if there are many objects on the table, placing actions may incur collisions.
# * Prompt saturation - if too many commands (10+) are executed in a row, then the LLM may start to ignore examples in the early parts of the prompt.
# * Ambiguous instructions - if a given instruction doesn't lead to the desired actions, try rephrasing it to remove ambiguities (e.g. place the block on the closest bowl -> place the block on its closest bowl)

# %%
prompt_tabletop_ui = '''
# Python 2D robot control script
import numpy as np
from env_utils import put_first_on_second, get_obj_pos, get_obj_names, say, get_corner_name, get_side_name, is_obj_visible, stack_objects_in_order
from plan_utils import parse_obj_name, parse_position, parse_question, transform_shape_pts

objects = ['yellow block', 'green block', 'yellow bowl', 'blue block', 'blue bowl', 'green bowl']
# the yellow block on the yellow bowl.
say('Ok - putting the yellow block on the yellow bowl')
put_first_on_second('yellow block', 'yellow bowl')
objects = ['yellow block', 'green block', 'yellow bowl', 'blue block', 'blue bowl', 'green bowl']
# which block did you move.
say('I moved the yellow block')
objects = ['yellow block', 'green block', 'yellow bowl', 'blue block', 'blue bowl', 'green bowl']
# move the green block to the top right corner.
say('Got it - putting the green block on the top right corner')
corner_pos = parse_position('top right corner')
put_first_on_second('green block', corner_pos)
objects = ['yellow block', 'green block', 'yellow bowl', 'blue block', 'blue bowl', 'green bowl']
# stack the blue bowl on the yellow bowl on the green block.
order_bottom_to_top = ['green block', 'yellow block', 'blue bowl']
say(f'Sure - stacking from top to bottom: {", ".join(order_bottom_to_top)}')
stack_objects_in_order(object_names=order_bottom_to_top)
objects = ['cyan block', 'white block', 'cyan bowl', 'blue block', 'blue bowl', 'white bowl']
# move the cyan block into its corresponding bowl.
matches = {'cyan block': 'cyan bowl'}
say('Got it - placing the cyan block on the cyan bowl')
for first, second in matches.items():
  put_first_on_second(first, get_obj_pos(second))
objects = ['cyan block', 'white block', 'cyan bowl', 'blue block', 'blue bowl', 'white bowl']
# make a line of blocks on the right side.
say('No problem! Making a line of blocks on the right side')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 30cm vertical line on the right with {len(block_names)} points')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
objects = ['yellow block', 'red block', 'yellow bowl', 'gray block', 'gray bowl', 'red bowl']
# put the small banana colored thing in between the blue bowl and green block.
say('Sure thing - putting the yellow block between the blue bowl and the green block')
target_pos = parse_position('a point in the middle betweeen the blue bowl and the green block')
put_first_on_second('yellow block', target_pos)
objects = ['yellow block', 'red block', 'yellow bowl', 'gray block', 'gray bowl', 'red bowl']
# can you cut the bowls in half.
say('no, I can only move objects around')
objects = ['yellow block', 'green block', 'yellow bowl', 'gray block', 'gray bowl', 'green bowl']
# stack the blocks on the right side with the gray one on the bottom.
say('Ok. stacking the blocks on the right side with the gray block on the bottom')
right_side = parse_position('the right side')
put_first_on_second('gray block', right_side)
order_bottom_to_top = ['gray block', 'green block', 'yellow block']
stack_objects_in_order(object_names=order_bottom_to_top)
objects = ['yellow block', 'green block', 'yellow bowl', 'blue block', 'blue bowl', 'green bowl']
# hide the blue bowl.
bowl_name = np.random.choice(['yellow bowl', 'green bowl'])
say(f'Sounds good! Hiding the blue bowl under the {bowl_name}')
put_first_on_second(bowl_name, 'blue bowl')
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# stack everything with the green block on top.
say('Ok! Stacking everything with the green block on the top')
order_bottom_to_top = ['blue bowl', 'pink bowl', 'green bowl', 'pink block', 'blue block', 'green block']
stack_objects_in_order(object_names=order_bottom_to_top)
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# move the grass-colored bowl to the left.
say('Sure - moving the green bowl left by 10 centimeters')
left_pos = parse_position('a point 10cm left of the green bowl')
put_first_on_second('green bowl', left_pos)
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# why did you move the red bowl.
say(f'I did not move the red bowl')
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# undo that.
say('Sure - moving the green bowl right by 10 centimeters')
left_pos = parse_position('a point 10cm right of the green bowl')
put_first_on_second('green bowl', left_pos)
objects = ['brown bowl', 'green block', 'brown block', 'green bowl', 'blue bowl', 'blue block']
# place the top most block to the corner closest to the bottom most block.
top_block_name = parse_obj_name('top most block', f'objects = {get_obj_names()}')
bottom_block_name = parse_obj_name('bottom most block', f'objects = {get_obj_names()}')
closest_corner_pos = parse_position(f'the corner closest to the {bottom_block_name}', f'objects = {get_obj_names()}')
say(f'Putting the {top_block_name} on the {get_corner_name(closest_corner_pos)}')
put_first_on_second(top_block_name, closest_corner_pos)
objects = ['brown bowl', 'green block', 'brown block', 'green bowl', 'blue bowl', 'blue block']
# move the brown bowl to the side closest to the green block.
closest_side_position = parse_position('the side closest to the green block')
say(f'Got it - putting the brown bowl on the {get_side_name(closest_side_position)}')
put_first_on_second('brown bowl', closest_side_position)
objects = ['brown bowl', 'green block', 'brown block', 'green bowl', 'blue bowl', 'blue block']
# place the green block to the right of the bowl that has the blue block.
bowl_name = parse_obj_name('the bowl that has the blue block', f'objects = {get_obj_names()}')
if bowl_name:
  target_pos = parse_position(f'a point 10cm to the right of the {bowl_name}')
  say(f'No problem - placing the green block to the right of the {bowl_name}')
  put_first_on_second('green block', target_pos)
else:
  say('There are no bowls that has the blue block')
objects = ['brown bowl', 'green block', 'brown block', 'green bowl', 'blue bowl', 'blue block']
# place the blue block in the empty bowl.
empty_bowl_name = parse_obj_name('the empty bowl', f'objects = {get_obj_names()}')
if empty_bowl_name:
  say(f'Ok! Putting the blue block on the {empty_bowl_name}')
  put_first_on_second('blue block', empty_bowl_name)
else:
  say('There are no empty bowls')
objects = ['brown bowl', 'green block', 'brown block', 'green bowl', 'blue bowl', 'blue block']
# move the other blocks to the bottom corners.
block_names = parse_obj_name('blocks other than the blue block', f'objects = {get_obj_names()}')
corners = parse_position('the bottom corners')
for block_name, pos in zip(block_names, corners):
  put_first_on_second(block_name, pos)
objects = ['brown bowl', 'green block', 'brown block', 'green bowl', 'blue bowl', 'blue block']
# move the red bowl a lot to the left of the blocks.
say('Sure! Moving the red bowl to a point left of the blocks')
left_pos = parse_position('a point 20cm left of the blocks')
put_first_on_second('red bowl', left_pos)
objects = ['pink block', 'gray block', 'orange block']
# move the pinkish colored block on the bottom side.
say('Ok - putting the pink block on the bottom side')
bottom_side_pos = parse_position('the bottom side')
put_first_on_second('pink block', bottom_side_pos)
objects = ['yellow bowl', 'blue block', 'yellow block', 'blue bowl']
# is the blue block to the right of the yellow bowl?
if parse_question('is the blue block to the right of the yellow bowl?', f'objects = {get_obj_names()}'):
  say('yes, there is a blue block to the right of the yellow bow')
else:
  say('no, there is\'t a blue block to the right of the yellow bow')
objects = ['yellow bowl', 'blue block', 'yellow block', 'blue bowl']
# how many yellow objects are there?
n_yellow_objs = parse_question('how many yellow objects are there', f'objects = {get_obj_names()}')
say(f'there are {n_yellow_objs} yellow object')
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# move the left most block to the green bowl.
left_block_name = parse_obj_name('left most block', f'objects = {get_obj_names()}')
say(f'Moving the {left_block_name} on the green bowl')
put_first_on_second(left_block_name, 'green bowl')
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# move the other blocks to different corners.
block_names = parse_obj_name(f'blocks other than the {left_block_name}', f'objects = {get_obj_names()}')
corners = parse_position('the corners')
say(f'Ok - moving the other {len(block_names)} blocks to different corners')
for block_name, pos in zip(block_names, corners):
  put_first_on_second(block_name, pos)
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# is the pink block on the green bowl.
if parse_question('is the pink block on the green bowl', f'objects = {get_obj_names()}'):
  say('Yes - the pink block is on the green bowl.')
else:
  say('No - the pink block is not on the green bowl.')
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# what are the blocks left of the green bowl.
left_block_names =  parse_question('what are the blocks left of the green bowl', f'objects = {get_obj_names()}')
if len(left_block_names) > 0:
  say(f'These blocks are left of the green bowl: {", ".join(left_block_names)}')
else:
  say('There are no blocks left of the green bowl')
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# if you see a purple bowl put it on the blue bowl
if is_obj_visible('purple bowl'):
  say('Putting the purple bowl on the pink bowl')
  put_first_on_second('purple bowl', 'pink bowl')
else:
  say('I don\'t see a purple bowl')
objects = ['yellow block', 'green block', 'yellow bowl', 'blue block', 'blue bowl', 'green bowl']
# imagine that the bowls are different biomes on earth and imagine that the blocks are parts of a building.
say('ok')
objects = ['yellow block', 'green block', 'yellow bowl', 'blue block', 'blue bowl', 'green bowl']
# now build a tower in the grasslands.
order_bottom_to_top = ['green bowl', 'blue block', 'green block', 'yellow block']
say('stacking the blocks on the green bowl')
stack_objects_in_order(object_names=order_bottom_to_top)
objects = ['yellow block', 'green block', 'yellow bowl', 'gray block', 'gray bowl', 'green bowl']
# show me what happens when the desert gets flooded by the ocean.
say('putting the yellow bowl on the blue bowl')
put_first_on_second('yellow bowl', 'blue bowl')
objects = ['pink block', 'gray block', 'orange block']
# move all blocks 5cm toward the top.
say('Ok - moving all blocks 5cm toward the top')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for block_name in block_names:
  target_pos = parse_position(f'a point 5cm above the {block_name}')
  put_first_on_second(block_name, target_pos)
objects = ['cyan block', 'white block', 'purple bowl', 'blue block', 'blue bowl', 'white bowl']
# make a triangle of blocks in the middle.
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
triangle_pts = parse_position(f'a triangle with size 10cm around the middle with {len(block_names)} points')
say('Making a triangle of blocks around the middle of the workspace')
for block_name, pt in zip(block_names, triangle_pts):
  put_first_on_second(block_name, pt)
objects = ['cyan block', 'white block', 'purple bowl', 'blue block', 'blue bowl', 'white bowl']
# make the triangle smaller.
triangle_pts = transform_shape_pts('scale it by 0.5x', shape_pts=triangle_pts)
say('Making the triangle smaller')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for block_name, pt in zip(block_names, triangle_pts):
  put_first_on_second(block_name, pt)
objects = ['brown bowl', 'red block', 'brown block', 'red bowl', 'pink bowl', 'pink block']
# put the red block on the farthest bowl.
farthest_bowl_name = parse_obj_name('the bowl farthest from the red block', f'objects = {get_obj_names()}')
say(f'Putting the red block on the {farthest_bowl_name}')
put_first_on_second('red block', farthest_bowl_name)
'''.strip()

# %%
prompt_parse_obj_name = '''
import numpy as np
from env_utils import get_obj_pos, parse_position
from utils import get_obj_positions_np

objects = ['blue block', 'cyan block', 'purple bowl', 'gray bowl', 'brown bowl', 'pink block', 'purple block']
# the block closest to the purple bowl.
block_names = ['blue block', 'cyan block', 'purple block']
block_positions = get_obj_positions_np(block_names)
closest_block_idx = get_closest_idx(points=block_positions, point=get_obj_pos('purple bowl'))
closest_block_name = block_names[closest_block_idx]
ret_val = closest_block_name
objects = ['brown bowl', 'banana', 'brown block', 'apple', 'blue bowl', 'blue block']
# the blocks.
ret_val = ['brown block', 'blue block']
objects = ['brown bowl', 'banana', 'brown block', 'apple', 'blue bowl', 'blue block']
# the brown objects.
ret_val = ['brown bowl', 'brown block']
objects = ['brown bowl', 'banana', 'brown block', 'apple', 'blue bowl', 'blue block']
# a fruit that's not the apple
fruit_names = ['banana', 'apple']
for fruit_name in fruit_names:
    if fruit_name != 'apple':
        ret_val = fruit_name
objects = ['blue block', 'cyan block', 'purple bowl', 'brown bowl', 'purple block']
# blocks above the brown bowl.
block_names = ['blue block', 'cyan block', 'purple block']
brown_bowl_pos = get_obj_pos('brown bowl')
use_block_names = []
for block_name in block_names:
    if get_obj_pos(block_name)[1] > brown_bowl_pos[1]:
        use_block_names.append(block_name)
ret_val = use_block_names
objects = ['blue block', 'cyan block', 'purple bowl', 'brown bowl', 'purple block']
# the blue block.
ret_val = 'blue block'
objects = ['blue block', 'cyan block', 'purple bowl', 'brown bowl', 'purple block']
# the block closest to the bottom right corner.
corner_pos = parse_position('bottom right corner')
block_names = ['blue block', 'cyan block', 'purple block']
block_positions = get_obj_positions_np(block_names)
closest_block_idx = get_closest_idx(points=block_positions, point=corner_pos)
closest_block_name = block_names[closest_block_idx]
ret_val = closest_block_name
objects = ['brown bowl', 'green block', 'brown block', 'green bowl', 'blue bowl', 'blue block']
# the left most block.
block_names = ['green block', 'brown block', 'blue block']
block_positions = get_obj_positions_np(block_names)
left_block_idx = np.argsort(block_positions[:, 0])[0]
left_block_name = block_names[left_block_idx]
ret_val = left_block_name
objects = ['brown bowl', 'green block', 'brown block', 'green bowl', 'blue bowl', 'blue block']
# the bowl on near the top.
bowl_names = ['brown bowl', 'green bowl', 'blue bowl']
bowl_positions = get_obj_positions_np(bowl_names)
top_bowl_idx = np.argsort(block_positions[:, 1])[-1]
top_bowl_name = bowl_names[top_bowl_idx]
ret_val = top_bowl_name
objects = ['yellow bowl', 'purple block', 'yellow block', 'purple bowl', 'pink bowl', 'pink block']
# the third bowl from the right.
bowl_names = ['yellow bowl', 'purple bowl', 'pink bowl']
bowl_positions = get_obj_positions_np(bowl_names)
bowl_idx = np.argsort(block_positions[:, 0])[-3]
bowl_name = bowl_names[bowl_idx]
ret_val = bowl_name
'''.strip()

# %%
prompt_parse_position = '''
import numpy as np
from shapely.geometry import *
from shapely.affinity import *
from env_utils import denormalize_xy, parse_obj_name, get_obj_names, get_obj_pos

# a 30cm horizontal line in the middle with 3 points.
middle_pos = denormalize_xy([0.5, 0.5])
start_pos = middle_pos + [-0.3/2, 0]
end_pos = middle_pos + [0.3/2, 0]
line = make_line(start=start_pos, end=end_pos)
points = interpolate_pts_on_line(line=line, n=3)
ret_val = points
# a 20cm vertical line near the right with 4 points.
middle_pos = denormalize_xy([1, 0.5])
start_pos = middle_pos + [0, -0.2/2]
end_pos = middle_pos + [0, 0.2/2]
line = make_line(start=start_pos, end=end_pos)
points = interpolate_pts_on_line(line=line, n=4)
ret_val = points
# a diagonal line from the top left to the bottom right corner with 5 points.
top_left_corner = denormalize_xy([0, 1])
bottom_right_corner = denormalize_xy([1, 0])
line = make_line(start=top_left_corner, end=bottom_right_corner)
points = interpolate_pts_on_line(line=line, n=5)
ret_val = points
# a triangle with size 10cm with 3 points.
polygon = make_triangle(size=0.1, center=denormalize_xy([0.5, 0.5]))
points = get_points_from_polygon(polygon)
ret_val = points
# the corner closest to the sun colored block.
block_name = parse_obj_name('the sun colored block', f'objects = {get_obj_names()}')
corner_positions = np.array([denormalize_xy(pos) for pos in [[0, 0], [0, 1], [1, 1], [1, 0]]])
closest_corner_pos = get_closest_point(points=corner_positions, point=get_obj_pos(block_name))
ret_val = closest_corner_pos
# the side farthest from the right most bowl.
bowl_name = parse_obj_name('the right most bowl', f'objects = {get_obj_names()}')
side_positions = np.array([denormalize_xy(pos) for pos in [[0.5, 0], [0.5, 1], [1, 0.5], [0, 0.5]]])
farthest_side_pos = get_farthest_point(points=side_positions, point=get_obj_pos(bowl_name))
ret_val = farthest_side_pos
# a point above the third block from the bottom.
block_name = parse_obj_name('the third block from the bottom', f'objects = {get_obj_names()}')
ret_val = get_obj_pos(block_name) + [0.1, 0]
# a point 10cm left of the bowls.
bowl_names = parse_obj_name('the bowls', f'objects = {get_obj_names()}')
bowl_positions = get_all_object_positions_np(obj_names=bowl_names)
left_obj_pos = bowl_positions[np.argmin(bowl_positions[:, 0])] + [-0.1, 0]
ret_val = left_obj_pos
# the bottom side.
bottom_pos = denormalize_xy([0.5, 0])
ret_val = bottom_pos
# the top corners.
top_left_pos = denormalize_xy([0, 1])
top_right_pos = denormalize_xy([1, 1])
ret_val = [top_left_pos, top_right_pos]
'''.strip()

# %%
prompt_parse_question = '''
from utils import get_obj_pos, get_obj_names, parse_obj_name, bbox_contains_pt, is_obj_visible

objects = ['yellow bowl', 'blue block', 'yellow block', 'blue bowl', 'fruit', 'green block', 'black bowl']
# is the blue block to the right of the yellow bowl?
ret_val = get_obj_pos('blue block')[0] > get_obj_pos('yellow bowl')[0]
objects = ['yellow bowl', 'blue block', 'yellow block', 'blue bowl', 'fruit', 'green block', 'black bowl']
# how many yellow objects are there?
yellow_object_names = parse_obj_name('the yellow objects', f'objects = {get_obj_names()}')
ret_val = len(yellow_object_names)
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# is the pink block on the green bowl?
ret_val = bbox_contains_pt(container_name='green bowl', obj_name='pink block')
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# what are the blocks left of the green bowl?
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
green_bowl_pos = get_obj_pos('green bowl')
left_block_names = []
for block_name in block_names:
  if get_obj_pos(block_name)[0] < green_bowl_pos[0]:
    left_block_names.append(block_name)
ret_val = left_block_names
objects = ['pink block', 'yellow block', 'pink bowl', 'blue block', 'blue bowl', 'yellow bowl']
# is the sun colored block above the blue bowl?
sun_block_name = parse_obj_name('sun colored block', f'objects = {get_obj_names()}')
sun_block_pos = get_obj_pos(sun_block_name)
blue_bowl_pos = get_obj_pos('blue bowl')
ret_val = sun_block_pos[1] > blue_bowl_pos[1]
objects = ['pink block', 'yellow block', 'pink bowl', 'blue block', 'blue bowl', 'yellow bowl']
# is the green block below the blue bowl?
ret_val = get_obj_pos('green block')[1] < get_obj_pos('blue bowl')[1]
'''.strip()

# %%
prompt_transform_shape_pts = '''
import numpy as np
from utils import get_obj_pos, get_obj_names, parse_position, parse_obj_name

# make it bigger by 1.5.
new_shape_pts = scale_pts_around_centroid_np(shape_pts, scale_x=1.5, scale_y=1.5)
# move it to the right by 10cm.
new_shape_pts = translate_pts_np(shape_pts, delta=[0.1, 0])
# move it to the top by 20cm.
new_shape_pts = translate_pts_np(shape_pts, delta=[0, 0.2])
# rotate it clockwise by 40 degrees.
new_shape_pts = rotate_pts_around_centroid_np(shape_pts, angle=-np.deg2rad(40))
# rotate by 30 degrees and make it slightly smaller
new_shape_pts = rotate_pts_around_centroid_np(shape_pts, angle=np.deg2rad(30))
new_shape_pts = scale_pts_around_centroid_np(new_shape_pts, scale_x=0.7, scale_y=0.7)
# move it toward the blue block.
block_name = parse_obj_name('the blue block', f'objects = {get_obj_names()}')
block_pos = get_obj_pos(block_name)
mean_delta = np.mean(block_pos - shape_pts, axis=1)
new_shape_pts = translate_pts_np(shape_pts, mean_delta)
'''.strip()

# %%
prompt_fgen = '''
import numpy as np
from shapely.geometry import *
from shapely.affinity import *

from env_utils import get_obj_pos, get_obj_names
from ctrl_utils import put_first_on_second

# define function: total = get_total(xs=numbers).
def get_total(xs):
    return np.sum(xs)

# define function: y = eval_line(x, slope, y_intercept=0).
def eval_line(x, slope, y_intercept):
    return x * slope + y_intercept

# define function: pt = get_pt_to_the_left(pt, dist).
def get_pt_to_the_left(pt, dist):
    return pt + [-dist, 0]

# define function: pt = get_pt_to_the_top(pt, dist).
def get_pt_to_the_top(pt, dist):
    return pt + [0, dist]

# define function line = make_line_by_length(length=x).
def make_line_by_length(length):
  line = LineString([[0, 0], [length, 0]])
  return line

# define function: line = make_vertical_line_by_length(length=x).
def make_vertical_line_by_length(length):
  line = make_line_by_length(length)
  vertical_line = rotate(line, 90)
  return vertical_line

# define function: pt = interpolate_line(line, t=0.5).
def interpolate_line(line, t):
  pt = line.interpolate(t, normalized=True)
  return np.array(pt.coords[0])

# example: scale a line by 2.
line = make_line_by_length(1)
new_shape = scale(line, xfact=2, yfact=2)

# example: put object1 on top of object0.
put_first_on_second('object1', 'object0')

# example: get the position of the first object.
obj_names = get_obj_names()
pos_2d = get_obj_pos(obj_names[0])
'''.strip()

# %% [markdown]
# ### LMP Config

# %%
# model_name = 'code-davinci-002'
model_name = 'text-davinci-003'

cfg_tabletop = {
  'lmps': {
    'tabletop_ui': {
      'prompt_text': prompt_tabletop_ui,
      'engine': model_name,
      'max_tokens': 256,
      'temperature': 0,
      'query_prefix': '# ',
      'query_suffix': '.',
      'stop': ['#', 'objects = ['],
      'maintain_session': True,
      'debug_mode': False,
      'include_context': True,
      'has_return': False,
      'return_val_name': 'ret_val',
    },
    'parse_obj_name': {
      'prompt_text': prompt_parse_obj_name,
      'engine': model_name,
      'max_tokens': 256,
      'temperature': 0,
      'query_prefix': '# ',
      'query_suffix': '.',
      'stop': ['#', 'objects = ['],
      'maintain_session': False,
      'debug_mode': False,
      'include_context': True,
      'has_return': True,
      'return_val_name': 'ret_val',
    },
    'parse_position': {
      'prompt_text': prompt_parse_position,
      'engine': model_name,
      'max_tokens': 256,
      'temperature': 0,
      'query_prefix': '# ',
      'query_suffix': '.',
      'stop': ['#'],
      'maintain_session': False,
      'debug_mode': False,
      'include_context': True,
      'has_return': True,
      'return_val_name': 'ret_val',
    },
    'parse_question': {
      'prompt_text': prompt_parse_question,
      'engine': model_name,
      'max_tokens': 256,
      'temperature': 0,
      'query_prefix': '# ',
      'query_suffix': '.',
      'stop': ['#', 'objects = ['],
      'maintain_session': False,
      'debug_mode': False,
      'include_context': True,
      'has_return': True,
      'return_val_name': 'ret_val',
    },
    'transform_shape_pts': {
      'prompt_text': prompt_transform_shape_pts,
      'engine': model_name,
      'max_tokens': 256,
      'temperature': 0,
      'query_prefix': '# ',
      'query_suffix': '.',
      'stop': ['#'],
      'maintain_session': False,
      'debug_mode': False,
      'include_context': True,
      'has_return': True,
      'return_val_name': 'new_shape_pts',
    },
    'fgen': {
      'prompt_text': prompt_fgen,
      'engine': model_name,
      'max_tokens': 256,
      'temperature': 0,
      'query_prefix': '# define function: ',
      'query_suffix': '.',
      'stop': ['# define', '# example'],
      'maintain_session': False,
      'debug_mode': False,
      'include_context': True,
    }
  }
}

lmp_tabletop_coords = {
        'top_left':     (-0.3 + 0.05, -0.2 - 0.05),
        'top_side':     (0,           -0.2 - 0.05),
        'top_right':    (0.3 - 0.05,  -0.2 - 0.05),
        'left_side':    (-0.3 + 0.05, -0.5,      ),
        'middle':       (0,           -0.5,      ),
        'right_side':   (0.3 - 0.05,  -0.5,      ),
        'bottom_left':  (-0.3 + 0.05, -0.8 + 0.05),
        'bottom_side':  (0,           -0.8 + 0.05),
        'bottom_right': (0.3 - 0.05,  -0.8 + 0.05),
        'table_z':       0.0,
      }
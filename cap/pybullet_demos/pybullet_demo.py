# %%
from cap.pybullet_demos.pybullet_weight_env_config import USE_MDETR, cfg_tabletop, lmp_tabletop_coords
from cap.pybullet_demos.pybullet_weight_env import PickPlaceEnv
from cap.lmp_warpper import LMP_wrapper
from cap.lmp import LMP, LMPFGen
from cap.world_model import setup_LMP
from shapely.geometry import *
from shapely.affinity import *
from moviepy.editor import ImageSequenceClip
import shapely
import openai
import numpy as np
import cv2
from PIL import Image
import os
import copy
import pickle
import matplotlib
import matplotlib.pyplot as plt
import pdb
from cap.experiments.evaluate_models import StateAugAgent, cleanup_preprompt

from cap.helpers.openai_endpoints import openai_api_key


# %%
high_resolution = True  # @param {type:"boolean"}
high_frame_rate = False  # @param {type:"boolean"}

# %%
# setup env and LMP
env = PickPlaceEnv(
    render=True,
    high_res=high_resolution,
    high_frame_rate=high_frame_rate,
    use_mdetr=USE_MDETR,
)
block_list = ["green block", "orange block", "pink block", "red block"]
bowl_list = ["green bowl", "red bowl"]
obj_list = block_list + bowl_list + ["table"]
env.obj_name_to_weight = {"green block": 4.0,
                        "orange block": 2.0,
                        "pink block": 8.0,
                        "red block": 4.0}
_ = env.reset(obj_list)

init_world_state = '''
    # world_state = {
    #     "relations": [],
    #     “green block": {},
    #     “orange block": {},
    #     "red block": {},
    #     “pink block": {},
    #     “red bowl”: {},
    #     "green bowl": {},
    # }
    '''

lmp_tabletop_ui, lmp_wm = setup_LMP(env, init_world_state)

task_description = ''' '''

state_aug_agent = StateAugAgent(task_description)
state_aug_agent.reset(init_world_state)

# display env
demo_img = cv2.cvtColor(env.get_camera_image(), cv2.COLOR_BGR2RGB)
cv2.imwrite('cap_cabinet_demo.png', demo_img)

print('available objects:')
print(obj_list)

env.cache_video = []

print('Running policy and recording video...')

user_query = 'init'
pre_image = Image.fromarray(np.array([0]), 'RGB')
action_list = []
plt.figure("Image")
plt.ion()
while True:
    img_change = False
    img = Image.fromarray(env.get_camera_image(), 'RGB')

    if img.tobytes() != pre_image.tobytes():
        img_change = True
        pre_image = img

    # img.show()
    plt.imshow(img)
    plt.title(user_query)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    action_list.append((img, user_query, img_change))
    print('========= current world state =========')
    print(lmp_wm.state)
    print('===========================')

    print('> ', end='')
    user_query = input()
    if user_query == "quit":
        break
    user_query = cleanup_preprompt(user_query)
    code_string = state_aug_agent.step(user_query)
    lmp_tabletop_ui.execute_code_string(user_query, code_string, context=lmp_wm.commented_state)

# save commands-images
img_command_save_path = "cap_disinfection_demo_images_commands.pkl"
with open(img_command_save_path, "wb") as file:
    pickle.dump(action_list, file)
    print ("image-command pairs saved!")

# load commands-images
with open(img_command_save_path, "rb") as file:
    loaded_list = pickle.load(file)
    for item in loaded_list:
        img, command, img_change = item
        plt.imshow(img)
        plt.title(command)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        print ("command: ", command)
        print ("image change: ", img_change)

# render video
if env.cache_video:
    rendered_clip = ImageSequenceClip(
        env.cache_video, fps=60 if high_frame_rate else 25)
    # display(rendered_clip.ipython_display(autoplay=1, loop=1))
    rendered_clip.write_videofile("cap_weight_demo.mp4")

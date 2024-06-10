import numpy as np
import pybullet
from cap.pybullet_demos.pybullet_env import PickPlaceEnv, Robotiq2F85
from cap.pybullet_demos.pybullet_env_config import (BLOCK_SIZE, BOUNDS, COLORS_LAB, COLORS_RGB,
                                 CORNER_POS, DEBUG, LAB_TH, PIXEL_SIZE)
np.random.seed(0)

class DisinfectionEnv(PickPlaceEnv):
    def __init__(self, render=False, high_res=False, high_frame_rate=False, use_mdetr=False):
        super().__init__(render, high_res, high_frame_rate, use_mdetr)
        self.dirty_object_list = []

    def step_sim_and_render(self):
        interval = 40 if self.high_frame_rate else 120
        if self.sim_step % interval == 0:
            self.update_dirty()
        super().step_sim_and_render()

    # update the dirty list based on object positions
    # seems that we only need to call this function at render_image()
    def update_dirty(self):
        for obj_name in self.obj_name_to_id.keys():
            if 'ball' in obj_name:
                pybullet.removeBody(self.obj_name_to_id[obj_name][0])

        new_dirty_list = self.dirty_object_list.copy()
        for obj_name in self.obj_name_to_id.keys():
            for dirty_obj_name in self.dirty_object_list:

                contact_pts = pybullet.getContactPoints(self.obj_name_to_id[obj_name][0], self.obj_name_to_id[dirty_obj_name][0])
                if (len(contact_pts) > 0) and ("block" in obj_name) and (obj_name not in new_dirty_list):
                    new_dirty_list.append(obj_name)

                # contact_pts = pybullet.getContactPoints(self.obj_name_to_id[dirty_obj_name][0], self.obj_name_to_id['disinfector'][0])
                # if len(contact_pts) > 0 and "block" in dirty_obj_name:
                #     if dirty_obj_name in new_dirty_list:
                #         new_dirty_list.remove(dirty_obj_name)
                if np.linalg.norm(self.get_obj_pos(dirty_obj_name)[0] - self.get_obj_pos('disinfector')[0]) < 0.05\
                     and (self.get_obj_pos(dirty_obj_name)[1] < 0.1) and "block" in dirty_obj_name:
                    if dirty_obj_name in new_dirty_list:
                        new_dirty_list.remove(dirty_obj_name)

                    # set block color to original color
                    object_color = COLORS_RGB[dirty_obj_name.split(' ')[0]]
                    pybullet.changeVisualShape(self.obj_name_to_id[dirty_obj_name][0], -1, rgbaColor=object_color)

        # remove duplicates
        self.dirty_object_list = new_dirty_list
        for dirty_obj_name in self.dirty_object_list:
            # set block color to dirty color
            if "block" in dirty_obj_name:
                xy, z_lower, z_upper, _ = self.get_obj_pos(dirty_obj_name)
                self.add_ball([xy[0], xy[1], (z_lower + z_upper) / 2])

    def add_ball(self, pos):
        # The size of the circles can be adjusted
        object_visual = pybullet.createVisualShape(pybullet.GEOM_SPHERE, radius = 0.05, rgbaColor=[1., 0., 0., 0.3], specularColor=[0., 0., 0.])
        ball_id = pybullet.createMultiBody(baseVisualShapeIndex = object_visual, basePosition=pos)
        ball_name = 'ball ' + str(ball_id)
        self.obj_name_to_id[ball_name] = (ball_id,)

    def exit(self):
        pybullet.disconnect()

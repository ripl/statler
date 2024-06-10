import numpy as np
import pybullet
from cap.pybullet_demos.pybullet_env import PickPlaceEnv, Robotiq2F85
from cap.pybullet_demos.pybullet_env_config import (BLOCK_SIZE, BOUNDS, COLORS_LAB, COLORS_RGB,
                                 CORNER_POS, DEBUG, LAB_TH, PIXEL_SIZE)

np.random.seed(0)

class WeightEnv(PickPlaceEnv):
    def __init__(self, render=False, high_res=False, high_frame_rate=False, use_mdetr=False):
        super().__init__(render, high_res, high_frame_rate, use_mdetr)
        self.obj_name_to_weight = {}

    def step_sim_and_render(self):
        interval = 40 if self.high_frame_rate else 120
        if self.sim_step % interval == 0:
            self.update_weight_circles()
        super().step_sim_and_render()

    # update the circles that indicate the weight of the blocks
    def update_weight_circles(self):
        # delete the old circles
        for obj_name in self.obj_name_to_id.keys():
            if 'circle' in obj_name:
                pybullet.removeBody(self.obj_name_to_id[obj_name][0])

        # when a set of blocks are contacting, we add a circle at the weighted
        # center of the blocks to indicate the total weight of the blocks
        obj_names = [obj_name for obj_name in self.obj_name_to_weight.keys() if 'block' in obj_name]
        for obj_name1 in obj_names:
            for obj_name2 in obj_names:
                contact_pts = pybullet.getContactPoints(self.obj_name_to_id[obj_name1][0], self.obj_name_to_id[obj_name2][0])
                if len(contact_pts) > 0:
                    # compute weighted xy center of the pair of blocks
                    xy1, _, _, _ = self.get_obj_pos(obj_name1)
                    xy2, _, _, _ = self.get_obj_pos(obj_name2)
                    total_weight = self.obj_name_to_weight[obj_name1] + self.obj_name_to_weight[obj_name2]
                    xy = (xy1 * self.obj_name_to_weight[obj_name1] + xy2 * self.obj_name_to_weight[obj_name2]) / total_weight
                    self.add_circle(total_weight, xy)

                    # remove the names from the list
                    obj_names.remove(obj_name1)
                    obj_names.remove(obj_name2)
                    break

        # if no contact is found, add a circle for the single block
        while len(obj_names) > 0:
            self.add_circle(self.obj_name_to_weight[obj_names[0]], self.get_obj_pos(obj_names[0])[0])
            obj_names.remove(obj_names[0])

    def add_circle(self, weight, xy):
        # The size of the circles can be adjusted
        circle_radius = np.sqrt(weight) * BLOCK_SIZE * 0.3
        object_visual = pybullet.createVisualShape(pybullet.GEOM_CYLINDER, radius = circle_radius,\
                                                length = 0.001, rgbaColor=[0., 0., 0., 1.], specularColor=[0., 0., 0.])
        circle_id = pybullet.createMultiBody(baseVisualShapeIndex = object_visual, basePosition=[xy[0], xy[1], 0.001])
        circle_name = 'circle ' + str(circle_id)
        self.obj_name_to_id[circle_name] = (circle_id,)
from collections import defaultdict
from copy import deepcopy
from typing import Tuple

import cv2
import imageio
import numpy as np
import torch
import torch.nn.functional as F
import torchvision.transforms as T
from PIL import Image
from scipy.spatial.transform import Rotation
from skimage.color import rgb2lab
from sklearn.decomposition import PCA
from torch.nn.functional import one_hot
from cap.envs.ur5_env_config import PLACE_MARGIN  # PREGRASP_HEIGHT, PREPLACE_HEIGHT,
from cap.envs.ur5_env_config import ALL_BLOCKS, COLORS_LAB, CORNER_POS, DEBUG, GRIPPER_CLOSE, LAB_TH, PICK_MARGIN_RATIO, PREGRASP_MARGIN, PREPLACE_MARGIN, USE_ROS
from cap.helpers.utils import plot_results, pt2uv, rescale_bboxes
from cap.helpers import logger

if USE_ROS:
    import rospy
    from sensor_msgs.msg import PointCloud2
    from cap.helpers.utils import get_pointcloud_rosmsg


class UR5Env():
    # Env class for UR5 that matches the lmp_wapper API
    def __init__(self, default_pos=None, use_mdetr=True) -> None:
        from cap.ur5_arm import UR5Arm
        self.success = None
        self.arm = UR5Arm(default_pos)
        self.gripper_margin = 0.11
        self.pick_margin_ratio = PICK_MARGIN_RATIO
        self.place_margin = PLACE_MARGIN
        self.plane_z = self.arm.limits[2][0]
        self.object_list = ALL_BLOCKS
        self.use_mdetr = use_mdetr
        if use_mdetr:
            self.model_pc = torch.hub.load('ashkamath/mdetr:main', 'mdetr_efficientnetB3_phrasecut', pretrained=False, return_postprocessor=False)
            self.model_pc.load_state_dict(torch.load('mdetr_ckpts/phrasecut_EB3_checkpoint.pth')['model_ema'])
            self.model_pc = self.model_pc.cuda()
            self.model_pc.eval()
        self.pca = PCA()
        if USE_ROS:
            rospy.init_node('ur5_env')
            self.pc_pub = rospy.Publisher('/pc_debug', PointCloud2, queue_size=1, latch=True)

    def get_obj_pose_from_name(self, obj_name, radius, request_callback=None) -> Tuple[np.ndarray, float, float]:
        # orientation is currently not implemented
        assert self.use_mdetr, 'temporarily, we assume to use mdetr'
        import re

        # obj_name = re.sub('Rubiks', 'Rubik\'s', obj_name)
        mean_xy, min_z, max_z, axes = self.get_block_geometry(obj_name, radius, request_callback)
        return mean_xy, min_z, max_z, axes
        # color = ''
        # for key in COLORS_LAB.keys():
        #     if key in obj_name:
        #         color = key
        #         break
        # if not color:
        #     raise Exception(obj_name, 'color not hardcoded')

        # return self.get_block_geometry(color)

    def render_image(self):
        rgb, depth = self.arm.get_rgbd()
        cam_K, cam_pose = self.arm.get_cam_pose()
        position = cam_pose[:3]
        orientation = cam_pose[3:]

        return rgb, depth, position, orientation, cam_K

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
        homogen_points = np.pad(points, padding, 'constant', constant_values=1)
        for i in range(3):
            points[Ellipsis, i] = np.sum(transform[i, :] * homogen_points, axis=-1)
        return points

    def reset(self):
        logger.info('Reset')
        self.arm.grasp(GRIPPER_CLOSE)  # open the gripper
        self.arm.moveto_xyz(self.arm.default_pose[:3])

    def get_ee_pos(self):
        return self.arm.get_cam_pose()

    def step(self, action):
        """Do pick and place motion primitive."""
        pick_pose, place_pose = action['pick'].copy(), action['place'].copy()
        pick_pose[2] += self.gripper_margin
        place_pose[2] += self.gripper_margin

        pregrasp_pose = deepcopy(pick_pose)
        pregrasp_pose[2] = pick_pose[2] + PREGRASP_MARGIN

        postgrasp_pose = deepcopy(pick_pose)
        postgrasp_pose[2] = self.arm.default_pose[2]

        preplace_pose = deepcopy(place_pose)
        # preplace_pose[2] = place_pose[2] + PREPLACE_MARGIN
        preplace_pose[2] = self.arm.default_pose[2]


        pregrasp_pos = pregrasp_pose[:3]
        preplace_pos = preplace_pose[:3]

        exec_list = [
            (logger.info, '== Running Pick =='),
            (logger.info, 'resetting...'),
            # (self.reset, None),

            # pick
            (logger.info, 'moving to pregrasp pose'),
            (self.arm.moveto_pose, pregrasp_pose),
            (logger.info, 'opening gripper'),
            (self.arm.open_grip, None),
            (logger.info, 'moving to pick pose'),
            (self.arm.moveto_pose, pick_pose),
            (logger.info, 'closing grip'),
            (self.arm.close_grip, None),
            (logger.info, 'moving to postgrasp pose'),
            (self.arm.moveto_pose, postgrasp_pose),

            # place
            (logger.info, '== Running Place =='),
            # (logger.info, 'resetting...'),
            # (self.arm.moveto_xyz, self.arm.default_pose[:3]),
            # (logger.info, 'resetting...done'),
            (self.arm.moveto_xyz, preplace_pos),
            (self.arm.moveto_pose, place_pose),
            (self.arm.open_grip, None),
            (self.arm.moveto_xyz, preplace_pos),
        ]

        self.success = True
        for fn, args in exec_list:
            if args is not None:
                ret = fn(args)
            else:
                ret = fn()

            if ret is not None and ret == 0:
                logger.info('Movement execution failed!!')
                self.success = False
                break

        # reset
        logger.info('resetting...')
        self.reset()
        logger.info('resetting...done')

    def step_sim_and_render():
        pass

    def on_top_of(self, obj_a, obj_b):
        """
        check if obj_a is on top of obj_b
        condition 1: l2 distance on xy plane is less than a threshold
        condition 2: obj_a is higher than obj_b
        """
        obj_a_pos = self.get_obj_pos(obj_a)
        obj_b_pos = self.get_obj_pos(obj_b)
        xy_dist = np.linalg.norm(obj_a_pos[0] - obj_b_pos[0])
        if obj_b in CORNER_POS:
            is_near = xy_dist < 0.06
            return is_near
        elif 'bowl' in obj_b:
            is_near = xy_dist < 0.06
            is_higher = obj_a_pos[1] > obj_b_pos[1]
            return is_near and is_higher
        else:
            is_near = xy_dist < 0.04
            is_higher = obj_a_pos[1] > obj_b_pos[1]
        return is_near and is_higher

    def get_text_mask(self, img_np, obj_name, return_plt=False):
        transform = T.Compose([
            T.Resize(800),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        img_pil = Image.fromarray(np.uint8(img_np))
        img_tensor = transform(img_pil).unsqueeze(0).cuda()

        # propagate through the model
        outputs = self.model_pc(img_tensor, [obj_name])

        # keep only predictions with 0.95+ confidence
        probas = 1 - outputs['pred_logits'].softmax(-1)[0, :, -1].cpu()
        max_prob, index = torch.max(probas, 0)
        # if max_prob < 0.95:
        #     return None
        keep = one_hot(index, len(probas)).to(bool)

        # Interpolate masks to the correct size
        w, h = img_pil.size
        masks = F.interpolate(outputs["pred_masks"], size=(h, w), mode="bilinear", align_corners=False)
        masks = masks.cpu()[0, keep].sigmoid() > 0.5

        if DEBUG:
            bboxes_scaled = rescale_bboxes(outputs['pred_boxes'].cpu()[0, keep], img_pil.size)

            tokenized = self.model_pc.detr.transformer.tokenizer.batch_encode_plus([obj_name], padding="longest", return_tensors="pt").to(img_tensor.device)

            # Extract the text spans predicted by each box
            positive_tokens = (outputs["pred_logits"].cpu()[0, keep].softmax(-1) > 0.1).nonzero().tolist()
            predicted_spans = defaultdict(str)
            for tok in positive_tokens:
                item, pos = tok
                if pos < 255:
                    span = tokenized.token_to_chars(0, pos)
                    predicted_spans[item] += " " + obj_name[span.start:span.end]

            labels = [predicted_spans[k] for k in sorted(list(predicted_spans.keys()))]
            img_or_plt = plot_results(img_pil, probas[keep], bboxes_scaled, labels, masks, obj_name, return_plt=return_plt)
            return masks.squeeze(), img_or_plt

        return masks.squeeze()

    def get_color_mask(self, img, color_name):
        '''
        Given
        1. rgb image of dimension Height x Width x 3
        2. query color as string
        return
        a per-pixel mask
        '''
        color = COLORS_LAB[color_name]
        img_lab = rgb2lab(img)
        mask = np.linalg.norm((img_lab - color)[..., 1:], axis=-1) < LAB_TH

        if DEBUG:
            t = (mask * 0.3)[..., None]
            return mask, ((1 - t) * img + t * np.full(3, 255)).astype(np.uint8)

        return mask

    def get_block_geometry(self, block_info, radius, request_callback=None) -> Tuple[np.ndarray, float, float]:
        '''
        Given:
            - query block info (color or object name)
            - radius of the 1st obj to determine empty space
        Return:
            - xy coordinate of the center of the block
            - minimum z of the block
            - maximum z of the block
            - principal axes
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
        if DEBUG:
            mask, img_plt = mask

        if block_info == 'empty space':
            logger.info('searching for empty space...')
            # erode mask
            radius = int(np.ceil(radius / np.median(depth[mask]) * intrinsics[0, 0]))
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * radius, 2 * radius))
            mask = cv2.erode(mask.numpy().astype(np.uint8), kernel).astype(np.bool)
            h, w = mask.shape
            border_x = int(0.15 * w)
            border_y = int(0.15 * h)
            mask[:border_y] = 0
            mask[-border_y:] = 0
            mask[:, :border_x] = 0
            mask[:, -border_x:] = 0
            if DEBUG:
                rgb[~mask] = (rgb[~mask] * 0.5).astype(np.uint8)
                imageio.imwrite('empty_space_erode.png', rgb)
            # select random point within mask
            mask_indices = np.argwhere(mask)
            idx = mask_indices[np.random.choice(len(mask_indices))]
            mask = np.zeros_like(mask).astype(np.uint8)
            cv2.circle(mask, tuple(idx[::-1]), int(radius * 0.6), 1, thickness=-1)
            mask = mask.astype(np.bool)
            if DEBUG:
                rgb[~mask] = (rgb[~mask] * 0.5).astype(np.uint8)
                imageio.imwrite('empty_space_final.png', rgb)
            top_ratio = 1
        else:
            top_ratio = 0.75

        block_coords = points[mask]
        # prune outliers far from the center
        center_coord = np.mean(block_coords, axis=0)
        dists = np.linalg.norm(block_coords - center_coord, axis=-1)
        block_coords = block_coords[dists < np.quantile(dists, 0.95)]
        # use top points to compute mean_xy and principal axes
        min_z = block_coords[:, 2].min()
        max_z = block_coords[:, 2].max()
        block_coords_top = block_coords[block_coords[:, 2] > max_z - (max_z - min_z) * top_ratio]
        mean_xy = block_coords_top[:, :2].mean(axis=0)
        self.pca.fit(block_coords_top[:, :2])
        axes = self.pca.components_ * np.sqrt(self.pca.explained_variance_)[:, None]

        if DEBUG:
            pts = np.tile(center_coord, (3, 1))
            pts[1:, :2] += axes * 3
            uvs = pt2uv(pts, np.linalg.inv(cam2base), intrinsics)
            cv2.arrowedLine(img_plt, uvs[0], uvs[1], (255, 0, 0))
            cv2.arrowedLine(img_plt, uvs[0], uvs[2], (0, 255, 0))

            fname = f'mdetr+pca_{block_info}.png'
            cv2.imwrite(fname, img_plt[..., ::-1])

            try:
                import time
                started = time.time()
                if request_callback is not None:
                    request_callback(img_plt[..., ::-1])
                elapsed = time.time() - started
                logger.info(f'posting image took {elapsed}')
            except Exception:
                import traceback
                logger.warn('sending request to flask failed.')
                traceback.print_exc()

            if USE_ROS:
                pc = np.concatenate((block_coords, [(0, 1, 0, 1)] * len(block_coords)), axis=1)
                pc = np.concatenate((pc, ((*mean_xy, (min_z + max_z) / 2, 1, 0, 0, 1),)), axis=0)
                pc_msg = get_pointcloud_rosmsg(pc, 'ur_arm_base')
                self.pc_pub.publish(pc_msg)
                # rospy.sleep(0.1)
                # logger.info()

        return mean_xy, min_z, max_z, axes

    def get_obj_pos(self, obj_name, radius=None, request_callback=None):
        logger.info('obj_name', obj_name)
        if isinstance(obj_name, list):
            obj_name = obj_name[0]

        obj_name = obj_name.replace('the', '').replace('_', ' ').strip()
        if obj_name in CORNER_POS:
            return np.float32(np.array(CORNER_POS[obj_name]))
        mean_xy, min_z, max_z, axes = self.get_obj_pose_from_name(obj_name, radius, request_callback)

        return mean_xy
    
    def get_obj_pose(self, obj_name, radius=None, request_callback=None):
        logger.info('obj_name', obj_name)
        if isinstance(obj_name, list):
            obj_name = obj_name[0]

        obj_name = obj_name.replace('the', '').replace('_', ' ').strip()
        if obj_name in CORNER_POS:
            return np.float32(np.array(CORNER_POS[obj_name]))
        mean_xy, min_z, max_z, axes = self.get_obj_pose_from_name(obj_name, radius, request_callback)
        return mean_xy, min_z, max_z, axes
    
    def get_color(self, obj_name):
        for color, rgb in COLORS_LAB.items():
            if color in obj_name:
                return rgb


if __name__ == '__main__':
    env = UR5Env(use_mdetr=True)
    env.reset()

    env.arm.get_rgbd()
    # for obj in env.object_list:
    #     env.get_block_geometry(obj)
    #     break

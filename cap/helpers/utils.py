import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import torch
from matplotlib.patches import Polygon
from skimage.measure import find_contours

from cap.envs.ur5_env_config import USE_ROS

if USE_ROS:
    import rospy
    from sensor_msgs.msg import PointCloud2, PointField
    from std_msgs.msg import Header

if USE_ROS:
    def get_pointcloud_rosmsg(points, parent_frame):
        """ Creates a point cloud message.

        Args:
            points: Nx7 array of xyz positions (m) and rgba colors (0..1)
            parent_frame: frame in which the point cloud is defined

        Returns:
            sensor_msgs/PointCloud2 message

        """
        ros_dtype = PointField.FLOAT32
        dtype = np.float32
        itemsize = np.dtype(dtype).itemsize

        header = Header(frame_id=parent_frame, stamp=rospy.Time.now())
        fields = [PointField(name=n, offset=i * itemsize, datatype=ros_dtype, count=1) for i, n in enumerate('xyzrgba')]
        data = points.astype(dtype).tobytes()

        return PointCloud2(
            header=header,
            height=1,
            width=points.shape[0],
            fields=fields,
            is_bigendian=False,
            point_step=itemsize * 7,
            row_step=itemsize * 7 * points.shape[0],
            data=data,
            is_dense=False
        )


def apply_mask(image, mask, color, alpha=0.5):
    """Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 1, image[:, :, c] * (1 - alpha) + alpha * color[c] * 255, image[:, :, c])
    return image


# colors for visualization
COLORS_PLOT = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
               [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]


def plot_results(pil_img, scores, boxes, labels, masks=None, plot_name='', return_plt=False):
    plt.figure(figsize=(16, 10))
    np_image = np.array(pil_img)
    ax = plt.gca()
    colors = COLORS_PLOT * 100
    if masks is None:
        masks = [None for _ in range(len(scores))]
    assert len(scores) == len(boxes) == len(labels) == len(masks)
    for s, (xmin, ymin, xmax, ymax), l, mask, c in zip(scores, boxes.tolist(), labels, masks, colors):
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, fill=False, color=c, linewidth=3))
        ax.text(xmin, ymin, f'{l}: {s:0.2f}', fontsize=15, bbox=dict(facecolor='white', alpha=0.8))

        if mask is None:
            continue
        np_image = apply_mask(np_image, mask, c)

        padded_mask = np.zeros((mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        for verts in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            p = Polygon(verts, facecolor="none", edgecolor=c)
            ax.add_patch(p)

    plt.imshow(np_image)
    plt.axis('off')
    plt.savefig('mdetr_{}.png'.format(plot_name))

    # fig = plt.figure()
    # fig.canvas.draw()
    # # width, height = fig.get_size_inches() * fig.get_dpi()
    # img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    # img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    if return_plt:
        return plt
    return np_image


# for output bounding box post-processing
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)


def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b


def pt2uv(pt, T, K):
    if pt.shape[-1] > 1:
        pt = pt[..., None]
    s = pt.shape
    if s[-2] == 3:
        pt = np.concatenate((pt, np.ones((*s[:-2], 1, 1))), axis=-2)
    uv = K @ T[:3] @ pt
    return np.round(uv[..., :2, 0] / uv[..., [2], 0]).astype(int)

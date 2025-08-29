import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from plyfile import PlyData
from collections import defaultdict

from color_generator import generate_colors  
from utils.ply_parser import read_ply_with_seg_ids

def plot_point_cloud_with_seg_ids(points, seg_ids, max_points_per_seg=500):
    unique_ids = sorted(set(seg_ids))
    colors = generate_colors(len(unique_ids))
    color_map = {sid: colors[i] for i, sid in enumerate(unique_ids)}

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    for sid in unique_ids:
        mask = (seg_ids == sid)
        pts = points[mask]

        # 降采样每类点
        if len(pts) > max_points_per_seg:
            idx = np.random.choice(len(pts), max_points_per_seg, replace=False)
            pts = pts[idx]

        color_rgb = color_map[sid]
        ax.scatter(
            pts[:, 0], pts[:, 1], pts[:, 2],
            s=20,
            color=[color_rgb],
            edgecolors='k',
            linewidths=0.1,
            alpha=0.85
        )

    # equal aspect ratio
    xlim = ax.get_xlim3d()
    ylim = ax.get_ylim3d()
    zlim = ax.get_zlim3d()

    x_range = xlim[1] - xlim[0]
    y_range = ylim[1] - ylim[0]
    z_range = zlim[1] - zlim[0]
    max_range = max(x_range, y_range, z_range)

    x_middle = np.mean(xlim)
    y_middle = np.mean(ylim)
    z_middle = np.mean(zlim)

    ax.set_xlim3d(x_middle - max_range / 2, x_middle + max_range / 2)
    ax.set_ylim3d(y_middle - max_range / 2, y_middle + max_range / 2)
    ax.set_zlim3d(z_middle - max_range / 2, z_middle + max_range / 2)


    ax.view_init(elev=30, azim=45)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python render_ply_matplotlib.py clouds.ply")
        exit(1)

    ply_path = sys.argv[1]
    points, seg_ids = read_ply_with_seg_ids(ply_path)
    plot_point_cloud_with_seg_ids(points, seg_ids, max_points_per_seg=2000)


# 测试方式
# python render_ply_matplotlib.py ply/clouds.ply
# python render_ply_matplotlib.py ply/gaussian.ply

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sys
from mpl_toolkits.mplot3d import Axes3D  

from color_generator import generate_colors  


def draw_colored_circles(n, per_row=10):
    colors = generate_colors(n)
    rows = (n + per_row - 1) // per_row
    fig, ax = plt.subplots(figsize=(per_row, rows * 1.5))
    ax.set_aspect('equal')
    ax.axis('off')

    for idx, color_rgb in enumerate(colors):
        col = idx % per_row
        row = idx // per_row
        circle = patches.Circle((col + 0.5, rows - row - 0.5), 0.4, color=color_rgb)
        ax.add_patch(circle)

    plt.xlim(0, per_row)
    plt.ylim(0, rows)
    plt.tight_layout()
    plt.show()

def draw_colored_stripe(n, per_row=10):
    colors = generate_colors(n)
    rows = (n + per_row - 1) // per_row
    fig, ax = plt.subplots(figsize=(per_row, rows))
    ax.axis('off')

    for idx, color_rgb in enumerate(colors):
        col = idx % per_row
        row = idx // per_row
        rect = patches.Rectangle((col, rows - row - 1), 1, 1, color=color_rgb)
        ax.add_patch(rect)

    plt.xlim(0, per_row)
    plt.ylim(0, rows)
    plt.tight_layout()
    plt.show()

def draw_random_cluster(n, points_per_cluster=200):
    colors = generate_colors(n)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')

    for i in range(n):
        center_x, center_y = np.random.uniform(0, 10), np.random.uniform(0, 10)
        points = np.random.normal(loc=(center_x, center_y), scale=0.3, size=(points_per_cluster, 2))
        color_rgb = colors[i]
        ax.scatter(points[:, 0], points[:, 1], s=10, color=color_rgb)

    ax.axis('off')
    plt.tight_layout()
    plt.show()

def draw_random_cluster_3d(n, points_per_cluster=200):
    colors = generate_colors(n)
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection='3d')

    for i in range(n):
        center = np.random.uniform(0, 10, size=3)
        points = np.random.normal(loc=center, scale=0.4, size=(points_per_cluster, 3))
        color_rgb = colors[i]
        ax.scatter(points[:, 0], points[:, 1], points[:, 2],
                   s=20, color=[color_rgb], edgecolors='k', linewidths=0.1, alpha=0.85)

    ax.view_init(elev=30, azim=45)  
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

def draw_random_barplot(n):
    """
    Draw 3 repeated bar groups, each containing 'n' bars with distinct colors.
    Each group is identical in structure but values vary.
    """
    import matplotlib.pyplot as plt

    colors = generate_colors(n)
    bar_width = 0.8  # Wider since no overlap
    group_count = 3
    gap = 1.0        # Gap between groups

    # X positions for each group (shifted n each time)
    x = np.arange(n)
    fig, ax = plt.subplots(figsize=(max(8, n * 1.2), 5))

    for g in range(group_count):
        shift = g * (n + gap)
        values = np.random.uniform(0.4, 1.0, size=n)
        errors = np.random.uniform(0.05, 0.1, size=n)

        edgecolors = (np.array(colors) * 0.9).clip(0, 1)  # Make edge colors slightly darker
        errorcolors = (np.array(colors) * 0.75).clip(0, 1)  # Make error colors even darker

        for i in range(n):
            ax.bar(
                x[i] + shift,
                values[i],
                yerr=errors[i],
                width=bar_width,
                color=colors[i],
                edgecolor=edgecolors[i],
                linewidth=2.0,
                capsize=4,
                error_kw={
                    'ecolor': errorcolors[i],
                    'elinewidth': 2.0,
                    'capthick': 1.2
                }
            )

    # X-axis ticks for categories centered on each group
    total_width = group_count * (n + gap)
    ax.set_xticks([(n / 2 - 0.5) + i * (n + gap) for i in range(group_count)])
    ax.set_xticklabels([f'Group {i+1}' for i in range(group_count)])

    ax.set_ylabel("Value")
    ax.set_title(f"{group_count} Repeated Bar Groups with {n} Classes")
    # ax.legend()
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 29
    mode = sys.argv[2] if len(sys.argv) > 2 else 'all'

    if mode == 'circle':
        draw_colored_circles(n)
    elif mode == 'stripe':
        draw_colored_stripe(n)
    elif mode == 'cluster':
        draw_random_cluster(n)
    elif mode == 'cluster3d':
        draw_random_cluster_3d(n)
    elif mode == 'plot':
        draw_random_barplot(n)
    elif mode == 'all':
        print("[1/5] Drawing colored circles...")
        draw_colored_circles(n)
        print("[2/5] Drawing colored stripe...")
        draw_colored_stripe(n)
        print("[3/5] Drawing random 2D cluster...")
        draw_random_cluster(n)
        print("[4/5] Drawing random 3D cluster...")
        draw_random_cluster_3d(n)
        print("[5/5] Drawing random bar plot...")
        draw_random_barplot(n)

    else:
        print(f"Unknown mode: {mode}. Use one of: circle, stripe, cluster, cluster3d, all.")

# 测试方法
# 参数一 颜色个数
# 参数二 绘图模式
# python colors_test.py 10
# python colors_test.py 20
# python colors_test.py 60
# python colors_test.py 30 all
# python colors_test.py 30 circle
# python colors_test.py 30 stripe
# python colors_test.py 30 cluster
# python colors_test.py 30 cluster3d
# python colors_test.py 5 plot
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sys
from mpl_toolkits.mplot3d import Axes3D  

from color_generator import generate_colors  

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
    

def draw_barplot():
    import matplotlib.pyplot as plt
    import numpy as np
    from color_generator import generate_colors

    methods = ["Ours", "SC-GS", "GARField", "MovingPart"]
    metrics = ["Time", "Distance", "Error", "Usability", "Fidelity"]

    raw_data = np.array([
        [144.99, 24.36, 4.30, 0.20, 0.50, 0.047, 4.32, 0.120, 4.61, 0.096],  # Ours
        [322.76, 42.73, 6.49, 0.42, 1.20, 0.171, 3.36, 0.114, 3.45, 0.104],  # SC-GS
        [341.42,114.03, 6.56, 1.65, 1.35, 0.161, 3.41, 0.137, 3.32, 0.117],  # GARField
        [348.36,113.56, 6.85, 1.67, 1.08, 0.165, 3.47, 0.154, 3.46, 0.111]   # MovingPart
    ])

    values = raw_data[:, [0, 1, 2, 4, 8]]
    errors = raw_data[:, [5, 6, 7, 9, 9]]

    n_methods = len(methods)
    n_metrics = len(metrics)

    colors = generate_colors(n_methods)
    edgecolors = (np.array(colors) * 0.9).clip(0, 1)
    errorcolors = (np.array(colors) * 0.75).clip(0, 1)

    bar_width = 0.18
    x = np.arange(n_metrics)

    fig, ax = plt.subplots(figsize=(10, 5))

    for i, (method, val_row, err_row) in enumerate(zip(methods, values, errors)):
        # pos = x + i * bar_width
        pos = x + i * (bar_width + 0.04)
        for j in range(n_metrics):
            ax.bar(
                pos[j],
                val_row[j],
                yerr=err_row[j],
                width=bar_width,
                color=colors[i],
                edgecolor=edgecolors[i],
                linewidth=2.0,
                capsize=4,
                error_kw={
                    'ecolor': errorcolors[i],
                    'elinewidth': 2.0,
                    'capthick': 1.2
                },
                label=method if j == 0 else None  # 防止重复图例
            )

    ax.set_xticks(x + (n_methods - 1) * bar_width / 2)
    ax.set_xticklabels(metrics)

    ax.set_ylabel("Metric Value")
    ax.set_title("Method Comparison Across Metrics")
    ax.legend()
    plt.tight_layout()
    plt.show()


# def draw_barplot_dual_y():
#     import matplotlib.pyplot as plt
#     import numpy as np
#     from color_generator import generate_colors

#     # === 调整字体大小 ===
#     fontsize_ticks = 14
#     fontsize_label = 16
#     fontsize_legend = 14


#     def add_significance(ax, x1, x2, y, text='***', dy=0.02, offset=0.01):
#         """
#         在给定 y 高度上画一个统一高度的桥，并标注显著性
#         dy: 小竖直线高度；offset: text 相对位置
#         """
#         ax.plot([x1, x1, x2, x2], [y, y + dy, y + dy, y], lw=1.5, c='black')
#         ax.text((x1 + x2) / 2, y + dy + offset, text,
#                 ha='center', va='bottom', fontsize=14, color='black')

#     methods = ["Ours", "SC-GS", "GARField", "MovingPart"]
#     metrics = ["Time", "Distance", "Error", "Usability", "Fidelity"]

#     raw_data = np.array([
#         # [144.99, 24.36, 4.30, 0.20, 0.50, 0.047, 4.32, 0.120, 4.61, 0.096],
#         # [322.76, 42.73, 6.49, 0.42, 1.20, 0.171, 3.36, 0.114, 3.45, 0.104],
#         # [341.42,114.03, 6.56, 1.65, 1.35, 0.161, 3.41, 0.137, 3.32, 0.117],
#         # [348.36,113.56, 6.85, 1.67, 1.08, 0.165, 3.47, 0.154, 3.46, 0.111]
#         [145.000, 12.554, 4.317, 0.169, 0.485, 0.019, 4.300, 0.557, 4.600, 0.583],
#         [323.824, 29.384, 6.613, 0.146, 1.270, 0.094, 3.350, 0.572, 3.450, 0.669],
#         [341.414, 16.831, 6.299, 0.133, 1.326, 0.090, 3.400, 1.068, 3.350, 0.726],
#         [349.347, 13.418, 7.332, 0.376, 1.121, 0.183, 3.500, 0.742, 3.500, 0.806]
#     ])

#     # 提取数据
#     time_vals = raw_data[:, 0]
#     time_errs = raw_data[:, 1]
#     other_vals = raw_data[:, [2, 4, 6, 8]]
#     other_errs = raw_data[:, [3, 5, 7, 9]]

#     n_methods = len(methods)
#     n_metrics = other_vals.shape[1]
#     colors = generate_colors(n_methods)
#     edgecolors = (np.array(colors) * 0.9).clip(0, 1)
#     errorcolors = (np.array(colors) * 0.75).clip(0, 1)

#     bar_width = 0.15
#     spacing = 0.04
#     time_x = -1.0
#     x = np.arange(n_metrics)

#     fig, ax1 = plt.subplots(figsize=(10, 5))
#     ax2 = ax1.twinx()

#     time_positions = []
#     time_tops = []

#     # === Time Bars ===
#     for i in range(n_methods):
#         pos = time_x + i * (bar_width + spacing)
#         time_positions.append(pos)
#         top = time_vals[i] + time_errs[i]
#         time_tops.append(top)

#         ax1.bar(
#             pos,
#             time_vals[i],
#             yerr=time_errs[i],
#             width=bar_width,
#             color=colors[i],
#             edgecolor=edgecolors[i],
#             linewidth=2.0,
#             capsize=4,
#             error_kw={
#                 'ecolor': errorcolors[i],
#                 'elinewidth': 2.0,
#                 'capthick': 1.2
#             },
#             label=methods[i] if n_metrics == 0 else None
#         )

#     all_other_positions = [[] for _ in range(n_metrics)]
#     all_other_tops = [[] for _ in range(n_metrics)]

#     for i, (method, val_row, err_row) in enumerate(zip(methods, other_vals, other_errs)):
#         pos = x + i * (bar_width + spacing)
#         for j in range(n_metrics):
#             all_other_positions[j].append(pos[j])
#             all_other_tops[j].append(val_row[j] + err_row[j])

#             ax2.bar(
#                 pos[j],
#                 val_row[j],
#                 yerr=err_row[j],
#                 width=bar_width,
#                 color=colors[i],
#                 edgecolor=edgecolors[i],
#                 linewidth=2.0,
#                 capsize=4,
#                 error_kw={
#                     'ecolor': errorcolors[i],
#                     'elinewidth': 2.0,
#                     'capthick': 1.2
#                 },
#                 label=method if j == 0 else None
#             )

#     # === X ticks ===
#     full_xticks = [time_x + (n_methods - 1) * (bar_width + spacing) / 2] + \
#                   list(x + (n_methods - 1) * (bar_width + spacing) / 2)
#     full_xticklabels = ["Time"] + metrics[1:]
#     ax1.set_xticks(full_xticks)
#     ax1.set_xticklabels(full_xticklabels)

#     # === Labels and legend ===
#     ax1.set_ylabel("Time (s)", color='black')
#     ax2.set_ylabel("Distance (m), Error (m), and Other Metrics", color='black')
#     handles, labels = ax2.get_legend_handles_labels()
#     ax2.legend(handles, methods, loc="upper right")

#     ours_idx = 0
#     dy = 0.15  # vertical stub height
#     offset = -0.15
#     # ystep_time = 3.0
#     time_scale = 500*1.1 / 10
#     ystep_time = 0.3 * time_scale
#     ystep_other = 0.3

#     # === Time 显著性桥 ===
#     base_time_y = max(time_tops) + 0.04
#     for i, other_idx in enumerate(range(1, n_methods)):
#         add_significance(
#             ax1,
#             time_positions[ours_idx],
#             time_positions[other_idx],
#             base_time_y + (i+1) * ystep_time,
#             text='***',
#             dy=dy * time_scale,
#             offset=offset * time_scale
#         )

#     # === Other Metrics 显著性桥 ===
#     for j in range(n_metrics):
#         base_other_y = max(all_other_tops[j]) + 0.04
#         for i, other_idx in enumerate(range(1, n_methods)):
#             add_significance(
#                 ax2,
#                 all_other_positions[j][ours_idx],
#                 all_other_positions[j][other_idx],
#                 base_other_y + (i+1) * ystep_other,
#                 text='**' if j == 2 and i == 1 else '***',
#                 dy=dy,
#                 offset=offset
#             )

#     # === 自动调整 ylim，防止 *** 超出 ===
#     ax1.set_ylim(top=max(time_tops) * 1.1 + 3 * ystep_time + 0.1)
#     max_other_y = max([max(t) for t in all_other_tops])
#     ax2.set_ylim(top=max_other_y * 1.1 + 3 * ystep_other + 0.1)


#     # 坐标轴刻度字体
#     ax1.tick_params(axis='both', labelsize=fontsize_ticks)
#     ax2.tick_params(axis='both', labelsize=fontsize_ticks)

#     # 坐标轴标签字体
#     ax1.set_ylabel("Time (s)", fontsize=fontsize_label, color='black')
#     ax2.set_ylabel("Distance (m), Error (m), and Other Metrics", fontsize=fontsize_label, color='black')

#     # 图例字体
#     handles, labels = ax2.get_legend_handles_labels()
#     ax2.legend(handles, methods, loc="upper right", fontsize=fontsize_legend)




#     plt.tight_layout()
#     plt.show()



def draw_barplot_dual_y():
    import matplotlib.pyplot as plt
    import numpy as np
    from color_generator import generate_colors

    # === 字体设置 ===
    fontsize_ticks = 14
    fontsize_label = 16
    fontsize_legend = 14

    def add_significance(ax, x1, x2, y, text='***', dy=0.02, offset=0.01):
        ax.plot([x1, x1, x2, x2], [y, y + dy, y + dy, y], lw=1.5, c='black')
        ax.text((x1 + x2) / 2, y + dy + offset, text,
                ha='center', va='bottom', fontsize=14, color='black')

    methods = ["Ours", "SC-GS", "GARField", "MovingPart"]
    metrics = ["Time", "Error", "Distance", "Usability", "Fidelity"]
    # metrics = ["Time", "Chamfer", "Manipulation", "Usability", "Fidelity"]

    raw_data = np.array([
        [145.000, 12.554, 0.485, 0.019, 4.317, 0.169, 4.300, 0.557, 4.600, 0.583],
        [323.824, 29.384, 1.270, 0.094, 6.613, 0.146, 3.350, 0.572, 3.450, 0.669],
        [341.414, 16.831, 1.326, 0.090, 6.299, 0.133, 3.400, 1.068, 3.350, 0.726],
        [349.347, 13.418, 1.121, 0.183, 7.332, 0.376, 3.500, 0.742, 3.500, 0.806]
    ])

    # === 数据分离 ===
    time_chamfer_vals = raw_data[:, [0, 2]]
    time_chamfer_errs = raw_data[:, [1, 3]]
    other_vals = raw_data[:, [4, 6, 8]]
    other_errs = raw_data[:, [5, 7, 9]]

    n_methods = len(methods)
    colors = generate_colors(n_methods)
    edgecolors = (np.array(colors) * 0.9).clip(0, 1)
    errorcolors = (np.array(colors) * 0.75).clip(0, 1)

    bar_width = 0.15
    spacing = 0.04
    x_time = -2.0
    x_chamfer = -1.0
    x_other = np.arange(3)

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    # === ax1: Time & Chamfer ===
    x_left = [x_time, x_chamfer]
    left_positions = [[] for _ in range(2)]
    left_tops = [[] for _ in range(2)]

    for j in range(2):  # Time & Chamfer
        for i in range(n_methods):
            pos = x_left[j] + i * (bar_width + spacing)
            val = time_chamfer_vals[i, j]
            err = time_chamfer_errs[i, j]

            # 对 Chamfer 缩放
            if j == 1:
                val *= 100
                err *= 100

            left_positions[j].append(pos)
            left_tops[j].append(val + err)

            ax1.bar(
                pos,
                val,
                yerr=err,
                width=bar_width,
                color=colors[i],
                edgecolor=edgecolors[i],
                linewidth=2.0,
                capsize=4,
                error_kw={
                    'ecolor': errorcolors[i],
                    'elinewidth': 2.0,
                    'capthick': 1.2
                },
                label=methods[i] if j == 0 else None
            )

    # === ax2: Distance, Usability, Fidelity ===
    all_other_positions = [[] for _ in range(3)]
    all_other_tops = [[] for _ in range(3)]

    for i, (method, val_row, err_row) in enumerate(zip(methods, other_vals, other_errs)):
        pos = x_other + i * (bar_width + spacing)
        for j in range(3):
            all_other_positions[j].append(pos[j])
            all_other_tops[j].append(val_row[j] + err_row[j])

            ax2.bar(
                pos[j],
                val_row[j],
                yerr=err_row[j],
                width=bar_width,
                color=colors[i],
                edgecolor=edgecolors[i],
                linewidth=2.0,
                capsize=4,
                error_kw={
                    'ecolor': errorcolors[i],
                    'elinewidth': 2.0,
                    'capthick': 1.2
                },
                label=method if j == 0 else None
            )

    # === xticks ===
    xticks_all = [
        x_time + (n_methods - 1) * (bar_width + spacing) / 2,
        x_chamfer + (n_methods - 1) * (bar_width + spacing) / 2
    ] + list(x_other + (n_methods - 1) * (bar_width + spacing) / 2)
    ax1.set_xticks(xticks_all)
    ax1.set_xticklabels(metrics)

    # === 显著性桥 ===
    dy = 0.15
    offset = -0.15
    ystep = 0.3
    left_scale = 480 * 1.0 / 10

    for j in range(2):  # Time & Chamfer
        base_y = max(left_tops[j]) + 0.04
        for i in range(1, n_methods):
            add_significance(
                ax1,
                left_positions[j][0],
                left_positions[j][i],
                base_y + i * ystep * left_scale,
                text='***',
                dy=dy * left_scale,
                offset=offset - 0.15 * left_scale
            )

    for j in range(3):  # Distance, Usability, Fidelity
        base_y2 = max(all_other_tops[j]) + 0.04
        for i in range(1, n_methods):
            add_significance(
                ax2,
                all_other_positions[j][0],
                all_other_positions[j][i],
                base_y2 + i * ystep,
                text='**' if j == 1 and i - 1 == 1 else '***',
                dy=dy,
                offset=offset
            )

    # === Y轴标签 ===
    ax1.set_ylabel("Time (s), and Chamfer Error ($\\times 10^{-2}$ m)", fontsize=fontsize_label, color='black')
    ax2.set_ylabel("Distance (m), and Subjective Ratings", fontsize=fontsize_label, color='black')

    # === 图例和字体 ===
    ax1.tick_params(axis='both', labelsize=fontsize_ticks)
    ax2.tick_params(axis='both', labelsize=fontsize_ticks)
    handles, labels = ax2.get_legend_handles_labels()
    ax2.legend(handles, methods, loc="upper right", fontsize=fontsize_legend)

    # === 自动调整 y 轴范围 ===
    ax1.set_ylim(top=max([max(t) for t in left_tops]) * 1.2 + 6 * ystep + 0.2)
    ax2.set_ylim(top=max([max(t) for t in all_other_tops]) * 1.1 + 3 * ystep + 0.2)

    plt.tight_layout()
    plt.show()




if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 29
    mode = sys.argv[2] if len(sys.argv) > 2 else 'all'

    # draw_random_barplot(n)
    # draw_barplot()
    draw_barplot_dual_y()


# 测试方法
# python cache/draw_plot.py 
# python draw_plot.py
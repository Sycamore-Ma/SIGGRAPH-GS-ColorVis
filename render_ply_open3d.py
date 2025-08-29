import open3d as o3d
import numpy as np

from color_generator import generate_colors
from utils.ply_parser import read_ply_with_attributes

def plot_with_open3d(points, seg_ids, max_points_per_seg=2000):
    unique_ids = sorted(set(seg_ids))
    colors = generate_colors(len(unique_ids))
    color_map = {sid: colors[i] for i, sid in enumerate(unique_ids)}

    all_points = []
    all_colors = []

    for sid in unique_ids:
        mask = (seg_ids == sid)
        pts = points[mask]

        # 降采样
        if len(pts) > max_points_per_seg:
            idx = np.random.choice(len(pts), max_points_per_seg, replace=False)
            pts = pts[idx]

        color_rgb = color_map[sid]
        color_array = np.tile(color_rgb, (pts.shape[0], 1))

        all_points.append(pts)
        all_colors.append(color_array)

    full_points = np.vstack(all_points)
    full_colors = np.vstack(all_colors)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(full_points)
    pcd.colors = o3d.utility.Vector3dVector(full_colors)

    o3d.visualization.draw_geometries([pcd], window_name="Open3D: Segmented Point Cloud")


def sephere_with_open3d(points, seg_ids, max_points_per_seg=20, use_lighting=True):
    unique_ids = sorted(set(seg_ids))
    colors = generate_colors(len(unique_ids))
    color_map = {sid: colors[i] for i, sid in enumerate(unique_ids)}

    geometries = []
    sphere_radius = 0.02  

    for sid in unique_ids:
        mask = (seg_ids == sid)
        pts = points[mask]

        if len(pts) > max_points_per_seg:
            idx = np.random.choice(len(pts), max_points_per_seg, replace=False)
            pts = pts[idx]

        color_rgb = color_map[sid]

        for pt in pts:
            sphere = o3d.geometry.TriangleMesh.create_sphere(radius=sphere_radius)
            # 光照控制开关
            if use_lighting:
                sphere.compute_vertex_normals()  # 光照所需法线
            sphere.translate(pt)
            sphere.paint_uniform_color(color_rgb)
            geometries.append(sphere)

    o3d.visualization.draw_geometries(
        geometries,
        window_name="Open3D: Point Sphere Cloud",
        mesh_show_back_face=True  # 防止球体背面不显示
    )

def gaussian_with_open3d(points, seg_ids, quaternions, scales, alphas=None, max_points_per_seg=20, use_lighting=True):
    unique_ids = sorted(set(seg_ids))
    colors = generate_colors(len(unique_ids))
    color_map = {sid: colors[i] for i, sid in enumerate(unique_ids)}

    geometries = []
    base_radius = 0.02  

    for sid in unique_ids:
        mask = (seg_ids == sid)
        pts = points[mask]
        quats = quaternions[mask]
        scals = scales[mask]
        alpha_vals = alphas[mask] if alphas is not None else None

        if len(pts) > max_points_per_seg:
            idx = np.random.choice(len(pts), max_points_per_seg, replace=False)
            pts = pts[idx]
            quats = quats[idx]
            scals = scals[idx]
            alpha_vals = alpha_vals[idx] if alpha_vals is not None else None

        color_rgb = color_map[sid]

        for i in range(len(pts)):
            pt = pts[i]
            quat = quats[i]
            scale_xyz = scals[i]

            sphere = o3d.geometry.TriangleMesh.create_sphere(radius=base_radius)
            # 光照控制开关
            if use_lighting:
                sphere.compute_vertex_normals()  
            # 各向异性缩放
            T_scale = np.eye(4)
            T_scale[0, 0] = scale_xyz[0] / base_radius
            T_scale[1, 1] = scale_xyz[1] / base_radius
            T_scale[2, 2] = scale_xyz[2] / base_radius
            sphere.transform(T_scale)

            # Apply rotation from quaternion
            R = o3d.geometry.get_rotation_matrix_from_quaternion(quat)
            sphere.rotate(R, center=(0, 0, 0))

            sphere.translate(pt)
            sphere.paint_uniform_color(color_rgb)

            geometries.append(sphere)

    o3d.visualization.draw_geometries(
        geometries,
        window_name="Open3D: Gaussian Sphere Cloud",
        mesh_show_back_face=True
    )



if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python render_ply_open3d.py clouds.ply")
        exit(1)

    ply_path = sys.argv[1]
    data = read_ply_with_attributes(ply_path, seg_key='seg_id_l4')
    points = data['points']
    seg_ids = data['seg_ids']
    colors = data['colors']
    quaternions = data['quaternion']
    scales = data['scale']
    alphas = data['alpha']  # open3d o3d.visualization.O3DVisualizer 支持透明度，目前测试不支持

    # 普通点云渲染
    plot_with_open3d(points, seg_ids, max_points_per_seg=500)
    # 球体点云渲染（测试遮挡效果，美化后光影需要在 blender 里面做渲染），球体实例化慢，需等待
    sephere_with_open3d(points, seg_ids, max_points_per_seg=100)
    sephere_with_open3d(points, seg_ids, max_points_per_seg=100, use_lighting=False)    
    # 高斯点云渲染（测试变形效果，美化后光影需要在 blender 里面做渲染），球体实例化慢，需等待
    gaussian_with_open3d(points, seg_ids, quaternions, scales, alphas, max_points_per_seg=100)
    gaussian_with_open3d(points, seg_ids, quaternions, scales, alphas, max_points_per_seg=100, use_lighting=False)


# 测试方式
# python render_ply_open3d.py ply/gaussian.ply
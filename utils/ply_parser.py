import numpy as np
from plyfile import PlyData

def read_ply_with_seg_ids(ply_path):
    """
    读取 PLY 文件，返回点坐标和分割 ID
    :param ply_path: PLY 文件路径
    :return: 点坐标 (N, 3) 和分割 ID (N,)
    """

    ply = PlyData.read(ply_path)
    vertex = ply['vertex']
    points = np.stack([vertex['x'], vertex['y'], vertex['z']], axis=-1)
    seg_ids = vertex['seg_id_l4']
    return points, seg_ids

def read_ply_with_attributes(ply_path, seg_key='seg_id_l4'):
    """
    读取 PLY 文件，返回点坐标、分割 ID、颜色、四元数旋转、缩放和透明度
    :param ply_path: PLY 文件路径
    :param seg_key: 分割 ID 的键名（默认为 'seg_id_l4'）
    :return: 字典，包含点坐标、分割 ID、颜色、四元数旋转、缩放和透明度
    """

    ply = PlyData.read(ply_path)
    vertex = ply['vertex']

    # 点坐标
    points = np.stack([vertex['x'], vertex['y'], vertex['z']], axis=-1)
    num_points = len(points)  # 新增：点数
    # 分割 ID（可选用 l1 / l2 / l3 / l4）
    seg_ids = np.array(vertex[seg_key])

    seg_ids_l1 = np.array(vertex['seg_id_l1'])
    seg_ids_l2 = np.array(vertex['seg_id_l2'])
    seg_ids_l3 = np.array(vertex['seg_id_l3'])
    seg_ids_l4 = np.array(vertex['seg_id_l4'])

    # RGB 颜色（0-255 转 0-1）
    if 'red' in vertex and 'green' in vertex and 'blue' in vertex:
        colors = np.stack([
            vertex['red'] / 255.0,
            vertex['green'] / 255.0,
            vertex['blue'] / 255.0
        ], axis=-1)
    else:
        colors = None

    # 四元数旋转
    if all(k in vertex for k in ['qw', 'qx', 'qy', 'qz']):
        quaternions = np.stack([
            vertex['qw'], vertex['qx'], vertex['qy'], vertex['qz']
        ], axis=-1)
    else:
        quaternions = None
    # 缩放
    if all(k in vertex for k in ['sx', 'sy', 'sz']):
        scales = np.stack([
            vertex['sx'], vertex['sy'], vertex['sz']
        ], axis=-1)
    else:
        scales = None
    # 透明度
    alpha = vertex['alpha'] if 'alpha' in vertex else None

    return {
        'points': points,
        'seg_ids': seg_ids,
        'colors': colors,
        'quaternion': quaternions,
        'scale': scales,
        'alpha': alpha,
        'num_points': num_points  # 新增字段
    }


def get_ply_point_count(ply_path):
    """
    获取 PLY 文件中点的数量
    :param ply_path: PLY 文件路径
    :return: 点的数量（整数）
    """
    ply = PlyData.read(ply_path)
    return ply['vertex'].count
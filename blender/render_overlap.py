import bpy
import sys
import os
import random
from mathutils import Vector
from datetime import datetime
import numpy as np
import math

MAX_CACHE_CNT_OF_POINTS = 70000  # 最大缓存点数 
RENDER_RATE = 0.9 # 渲染点数比例

# 3840*2160, 1920*1080, 1440*1440, 1080*1080, 720*480
RENDER_WIDTH = 1440
RENDER_HEIGHT = 1440

GAUSSIAN_ON = True  # 是否使用高斯点云
# GAUSSIAN_ON = False  # 是否使用高斯点云

BASE_RADIUS = 0.01  # 球体半径
OVERALL_ALPHA = 1.0

MANUAL_CAM_ATTRIBUTE = True  # 是否手动设置相机属性
# MANUAL_CAM_ATTRIBUTE = False  # 是否手动设置相机属性

# FLIP_COORD = False  # 是否翻转坐标系
FLIP_COORD = True  # 是否翻转坐标系

# 2.8, 2.0, 2.0
CAM_DIS_EXTEND = 1.25  # 相机距离点云最大距离的扩展比例

TRIM_ALPHA = True  # 是否裁剪透明度（仅在高斯点云时使用）
# TRIM_ALPHA = False  # 是否裁剪透明度（仅在高斯点云时使用）

ply_paths = [
    "E:/SIGGRAPH-GS-ColorVis/ply/Teaser_robotic_PLY/robotic_t1.ply",
    # "E:/SIGGRAPH-GS-ColorVis/ply/Teaser_robotic_PLY/robotic_t2.ply",
    # "E:/SIGGRAPH-GS-ColorVis/ply/Teaser_robotic_PLY/robotic_t3.ply",
    "E:/SIGGRAPH-GS-ColorVis/ply/Teaser_robotic_PLY/robotic_t4.ply" 
]

# ply_paths = [
#     "E:/SIGGRAPH-GS-ColorVis/ply/Teaser_hook_PLY/hook_0.0.ply",
#     # "E:/SIGGRAPH-GS-ColorVis/ply/Teaser_hook_PLY/hook_0.5.ply",
#     "E:/SIGGRAPH-GS-ColorVis/ply/Teaser_hook_PLY/hook_0.7.ply" 
# ]

seg_key = 'seg_id_l4'  # ['seg_id_l1', 'seg_id_l2', 'seg_id_l3', 'seg_id_l4']   

# 添加项目根路径，便于导入 utils 模块
project_root = "E:/SIGGRAPH-GS-ColorVis"
sys.path.append(project_root)

from color_generator import generate_colors
from color_generator import adjust_saturation
from utils.ply_parser import read_ply_with_attributes  # 导入自定义的 ply 文件读取函数
from utils.ply_parser import get_ply_point_count

# === 配置路径 ===
def get_output_path():
    png_dir = "E:/SIGGRAPH-GS-ColorVis/blender/png"        # 输出渲染图片的文件夹
    os.makedirs(png_dir, exist_ok=True)                     # 自动创建输出目录（如不存在）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")    # 当前时间戳
    output_filename = f"blender_render_{timestamp}.png"     # 输出图片文件名
    output_path = os.path.join(png_dir, output_filename)    # 完整输出路径
    return output_path


# === 清空场景中已有的物体 === (blender 默认立方体)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# material_map = {}


for ply_i in range(len(ply_paths)):
    ply_path = ply_paths[ply_i]

    # === 读取点云数据 ===
    data = read_ply_with_attributes(ply_path, seg_key)
    points = data['points']        
    seg_ids = data['seg_ids']       
    # colors = data['colors']         
    quaternions = data['quaternion']  
    scales = data['scale']      
    alpha = data['alpha']      
    cnt = data['num_points']  


    # === 每个 seg_id 降采样为最多 20 个点 ===
    unique_ids = sorted(set(seg_ids))
    seg_masked_points = []
    seg_masked_ids = []
    seg_masked_quaternions = []
    seg_masked_scales = []
    seg_masked_alpha = []

    for sid in unique_ids:
        mask = (seg_ids == sid)

        group_pts = points[mask]
        group_qua = quaternions[mask]
        group_sca = scales[mask]
        group_alpha = alpha[mask] if alpha is not None else None

        # count = min(len(group_pts), 2000)  # 限制每个分组最多 20 个点
        # count = int(len(group_pts) * 0.075)  # 限制每个分组最多 20%
        # count = int(len(group_pts) * 0.33)  # 限制每个分组最多 20%
        # count = int(len(group_pts) * 0.033)  # 限制每个分组最多 20%
        # count = int(len(group_pts) * 1.0)  # 限制每个分组最多 20%

        rate = RENDER_RATE / cnt * MAX_CACHE_CNT_OF_POINTS / len(ply_paths)
        count = int(len(group_pts) * rate)  # 限制每个分组最多 20%

        if count == 0:
            continue  # 跳过空采样组

        indices = np.random.choice(len(group_pts), count, replace=False)

        seg_masked_points.append(group_pts[indices])
        seg_masked_ids.extend([sid] * count)
        seg_masked_quaternions.append(group_qua[indices])
        seg_masked_scales.append(group_sca[indices])
        if group_alpha is not None:
            seg_masked_alpha.append(group_alpha[indices])

    # 合并降采样结果
    points = np.vstack(seg_masked_points)
    seg_ids = np.array(seg_masked_ids)
    quaternions = np.vstack(seg_masked_quaternions)
    scales = np.vstack(seg_masked_scales)
    if alpha is not None:
        alpha = np.concatenate(seg_masked_alpha)




    # === ✅ 修正：重新提取实际保留的 seg_id（非常重要！）===
    actual_ids = sorted(set(seg_ids))  # 用于配色
    print(seg_ids)
    print(actual_ids)
    # _ = input("Press Enter to continue...")  # 等待用户输入
    colors = generate_colors(len(actual_ids))  # 按实际数量生成颜色

    # colors = adjust_saturation(colors, 2.0)  # 调整饱和度，因为在强光条件下，饱和度会很淡
    colors = adjust_saturation(colors, 1.4)  # 调整饱和度，因为在强光条件下，饱和度会很淡

    color_map = {sid: colors[ply_i] for ply_i, sid in enumerate(actual_ids)}

    # === 清空场景中已有的物体 ===
    # # bpy.ops.object.select_all(action='SELECT')
    # # bpy.ops.object.delete(use_global=False)

    # === 添加摄像机和光源 ===
    bpy.ops.object.camera_add(location=(3, -3, 2))                 # 摄像机放在 (3, -3, 2)
    bpy.context.scene.camera = bpy.context.object                 # 设置为当前场景使用的摄像机
    bpy.ops.object.light_add(type='SUN', location=(2, 2, 4))       # 添加一个太阳光源
    sun = bpy.context.object
    sun.data.energy = 0.1  # 光源强度，推荐值 1.0 ~ 10.0
    sun.data.angle = 0.5  # 单位为弧度，推荐值 0.1 ~ 1.0，越大阴影越软


    # === 添加主光（正上方） ===
    if FLIP_COORD is False:
        bpy.ops.object.light_add(type='SUN', location=(0, 0, 5))
    else:
        bpy.ops.object.light_add(type='SUN', location=(0, 5, 0))
    key_light = bpy.context.object
    key_light.name = "KeyLight"
    key_light.data.energy = 0.04
    key_light.data.angle = 0.2  # 软阴影

    # === 添加辅光（前下方，较弱） ===
    if FLIP_COORD is False:
        bpy.ops.object.light_add(type='SUN', location=(3, -3, 2))
    else:
        bpy.ops.object.light_add(type='SUN', location=(3, 2, -3))
    fill_light = bpy.context.object
    fill_light.name = "FillLight"
    fill_light.data.energy = 0.01
    fill_light.data.angle = 0.5

    # === 添加轮廓光（背后） ===
    if FLIP_COORD is False:
        bpy.ops.object.light_add(type='SUN', location=(-4, 4, 3))
    else:
        bpy.ops.object.light_add(type='SUN', location=(-4, 3, 4))
    rim_light = bpy.context.object
    rim_light.name = "RimLight"
    rim_light.data.energy = 0.025
    rim_light.data.angle = 0.3
    # 为 rim light 设置稍微偏蓝/冷色调，更凸显边缘：
    rim_light.data.color = (0.8, 0.9, 1.0)  # 淡蓝光


    # === 调整渲染、光影效果 ===
    bpy.context.scene.render.resolution_x = RENDER_WIDTH  
    bpy.context.scene.render.resolution_y = RENDER_HEIGHT  
    bpy.context.scene.render.resolution_percentage = 100  # 100% 全尺寸

    # 渲染引擎
    # bpy.context.scene.render.engine = 'BLENDER_EEVEE' # 更快
    bpy.context.scene.render.engine = 'CYCLES'                 # 渲染器设为 Cycles
    bpy.context.scene.cycles.transparent_max_bounces = 10       # 透明物体最大反弹次数
    bpy.context.scene.cycles.transparent_min_bounces = 3        # 透明物体最小反弹次数
    bpy.context.scene.cycles.samples = 64                      # 渲染采样数量（可调）
    bpy.context.scene.cycles.use_adaptive_sampling = True      # 自适应采样加速收敛
    bpy.context.scene.cycles.device = 'GPU'                    # 若有显卡，强烈推荐启用

    # 光照增强
    # bpy.context.scene.eevee.use_bloom = True
    # bpy.context.scene.eevee.use_gtao = True
    # bpy.context.scene.eevee.use_ssr = True

    # 对比度增强
    bpy.context.scene.view_settings.view_transform = 'Standard'
    # bpy.context.scene.view_settings.look = 'High Contrast'
    # bpy.context.scene.view_settings.view_transform = 'Filmic'
    # bpy.context.scene.view_settings.look = 'Medium High Contrast'


    # 背景设为纯白（不使用渐变 world）
    bpy.context.scene.world.use_nodes = False
    # === 调整光影效果完毕 ===



    # === 创建一个球体模板数据（只一个 mesh 数据） ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=BASE_RADIUS, location=(0, 0, 0))
    sphere_template = bpy.context.object
    sphere_template.name = "SphereTemplate"
    bpy.ops.object.shade_smooth()                  # 平滑球体表面
    # sphere_template.hide_viewport = True           # 在视图中隐藏模板球体
    # sphere_template.hide_render = True             # 渲染时也不显示模板球体

    mesh_template = sphere_template.data  # 单一 mesh 数据共用

    # 删除原始球体对象（避免渲染出来）
    sphere_mesh_data = sphere_template.data  # ✅ 保存 mesh 数据
    sphere_obj_data = sphere_template        # ✅ 保存 object 对象（拷贝结构）
    # bpy.ops.object.delete()




    # === 准备材质映射，每个 seg_id 一个材质 ===
    material_map = {}
    for sid in set(seg_ids):
        # mat_name = f"Mat_{sid}"
        mat_name = f"Mat_{sid}_{ply_path.split('/')[-1].split('.')[0]}_{seg_key}_{ply_i}"
        if mat_name not in bpy.data.materials:
            if GAUSSIAN_ON is False:
                mat = bpy.data.materials.new(name=mat_name)
                mat.use_nodes = True
                bsdf = mat.node_tree.nodes["Principled BSDF"]
                # bsdf.inputs["Base Color"].default_value = color_map[sid] + [1.0]  # RGBA，Alpha=1
                bsdf.inputs["Base Color"].default_value = color_map[sid] + (1.0,)  # RGB + Alpha
                # bsdf.inputs["Base Color"].default_value = color_map[sid] + (0.1,)  # RGB + Alpha
                rgba = bsdf.inputs["Base Color"].default_value
                print(">>> ", color_map[sid])
                print(">>> ", rgba[:])
                material_map[sid] = mat
            else:
                # === 创建支持透明度的材质节点 ===
                mat = bpy.data.materials.new(name=mat_name)
                mat.use_nodes = True
                nodes = mat.node_tree.nodes
                links = mat.node_tree.links

                # 清空默认节点
                for n in nodes:
                    nodes.remove(n)

                # 创建 Output 节点
                output_node = nodes.new(type='ShaderNodeOutputMaterial')
                output_node.location = (400, 0)

                # 创建 Principled BSDF
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                principled.location = (0, 0)
                principled.inputs["Base Color"].default_value = color_map[sid] + (1.0,)  # RGBA
                # principled.inputs["Alpha"].default_value = 0.5  # 可调节透明度 0.0~1.0
                # principled.inputs["Alpha"].default_value = OVERALL_ALPHA / len(ply_paths) * (ply_i+1)

                if ply_i == 0:
                    # principled.inputs["Alpha"].default_value = OVERALL_ALPHA / 8
                    principled.inputs["Base Color"].default_value = (0.8, 0.8, 0.8) + (1.0,)  # RGBA
                    # principled.inputs["Alpha"].default_value = OVERALL_ALPHA / 5 
                    principled.inputs["Alpha"].default_value = OVERALL_ALPHA / 2             
                elif ply_i == 1:
                    principled.inputs["Alpha"].default_value = OVERALL_ALPHA

                # 连接 BSDF → 输出
                links.new(principled.outputs[0], output_node.inputs[0])

                # 启用透明混合和阴影
                mat.blend_method = 'BLEND'        # 可选: 'HASHED', 'CLIP'

                if ply_i == 0:
                    mat.shadow_method = 'NONE'  # 不投射阴影
                    bpy.context.scene.cycles.transparent_shadow = True
                    mat.use_backface_culling = True
                elif ply_i == 1:
                    mat.shadow_method = 'HASHED'      # Cycles 阴影支持透明
                    mat.use_backface_culling = False

                material_map[sid] = mat



    # === 为每个点创建实例或复制体 ===
    for i in range(len(points)):
        pt = points[i]

        if ply_i == 0:
            # pt = pt + Vector((0, 0.6, 0))  # 平移到 Z=0
            pt = pt + Vector((0, 0, 0.9))  # 平移到 Z=0

        sid = seg_ids[i]

        qua = quaternions[i]
        scale = scales[i]
        alp = alpha[i] if alpha is not None else 0.0

        # 选项一：直接使用模板球体实例化
        # instance = bpy.data.objects.new(f"Instance_{i}", mesh_template)

        # 选项二：复制模板球体数据，创建独立的 mesh 对象
        # 为每个球创建独立 mesh 对象，支持独立材质应用
        instance = sphere_obj_data.copy()
        instance.data = sphere_mesh_data.copy()

        if GAUSSIAN_ON:
            # 高斯点云
            instance.scale = Vector((scale[0] / BASE_RADIUS, scale[1] / BASE_RADIUS, scale[2] / BASE_RADIUS))
            # instance.scale = Vector((scale[0] * 0.01, scale[1] * 0.01, scale[2] * 0.01))
            instance.rotation_mode = 'QUATERNION'
            instance.rotation_quaternion = Vector(qua.tolist())



        instance.location = Vector(pt.tolist())
        instance.name = f"Instance_{i}"


        instance.location = Vector(pt.tolist())

        mat = material_map[sid]
        instance.data.materials.clear()
        instance.data.materials.append(mat)

        if TRIM_ALPHA and GAUSSIAN_ON:
            # 跳过透明度低的、形变量过大导致穿模的、超特大的点
            # if alp < 0.075:     
            #     continue  
            # if max(scale) / min(scale) > 1000.0:
            #     continue  
            # if max(scale) > 0.5:
            #     continue
            # if max(scale) / min(scale) > 1000.0 and max(scale) > 0.5:
            #     continue
            mid_scale = sum(scale) - max(scale) - min(scale)
            if max(scale) / min(scale) > 1000.0 and mid_scale > 0.02:
                continue
            if max(scale) > 0.5:
                continue
            if max(scale) > 0.075 and alp < 0.1:
                continue
            if max(scale) > 0.05 and alp < 0.05:
                continue
        bpy.context.collection.objects.link(instance)

    # === 添加地面平面（自动放在点云正下方） ===
    if FLIP_COORD is False:
        z_min = points[:, 2].min()
        plane_height = z_min - 0.02  # 稍微离点云底部远一点
        bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, plane_height))
    else:
        y_min = points[:, 1].min()
        plane_height = y_min - 0.02  # 稍微离点云底部远一点
        bpy.ops.mesh.primitive_plane_add(
            size=10, 
            location=(0, plane_height, 0),
            rotation=(math.radians(90), 0, 0)  # 绕 X 轴旋转 90 度，使法向量从 Z 变为 Y
        )


    ground = bpy.context.object
    ground.name = "GroundPlane"

    # 创建白色材质（也可微调为淡灰）
    ground_mat = bpy.data.materials.new(name="Mat_Ground")
    ground_mat.use_nodes = True
    bsdf = ground_mat.node_tree.nodes["Principled BSDF"]
    # bsdf.inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1.0)  # 纯白
    bsdf.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)  # 纯白
    ground.data.materials.append(ground_mat)

    # 接受阴影，默认启用，无需额外设置



    from mathutils import Vector, Matrix

    def set_cam_attributes_explicity(camera, direction, up=Vector((0, 1, 0))):
        right = direction.cross(up).normalized()
        true_up = right.cross(direction).normalized()

        rot_matrix = Matrix((
            right,
            true_up,
            -direction
        )).transposed()  # Blender expects column-major

        camera.rotation_euler = rot_matrix.to_euler()




    # === 自动对准相机并拉远 ===
    if MANUAL_CAM_ATTRIBUTE is False:
        center = sum((Vector(p.tolist()) for p in points), Vector()) / len(points)
        points_np = np.array([p.tolist() for p in points])
        max_range = np.max(points_np.max(axis=0) - points_np.min(axis=0))  # 点云尺寸
        cam = bpy.context.scene.camera
        cam_distance = max_range * CAM_DIS_EXTEND  # 可根据需要扩大比例
        # cam.location = center + Vector((cam_distance, -cam_distance, cam_distance*0.75))
        cam.location = center + Vector((-cam_distance, -cam_distance, cam_distance*0.75))
        # cam.location = center + Vector((-cam_distance, cam_distance, cam_distance*0.75))
        # cam.location = center + Vector((cam_distance, cam_distance, cam_distance*0.75))
        direction = center - cam.location
        cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    else:
        cam = bpy.context.scene.camera
        # location = Vector((-3.737691, -0.5309475, 1.4134218))
        # direction = Vector((0.92720693, 0.13171186, -0.35062674))
        # location = Vector((4.32 * 3.0, 0.76 * 3.0, 0.37 * 3.0))
        location = Vector((4.32 * 2, 0.76, 0.0))
        # location = Vector((4.32 * 2, 0. * 2, 0. * 2))


        # direction = Vector((-1.0, 0.0, 0.0))  
        points_np = np.array([p.tolist() for p in points])
        max_range = np.max(points_np.max(axis=0) - points_np.min(axis=0))  # 点云尺寸
        cam = bpy.context.scene.camera
        cam_distance = max_range * CAM_DIS_EXTEND  # 可根据需要扩大比例
        center = sum((Vector(p.tolist()) for p in points), Vector()) / len(points)
        cam.location = center + Vector((cam_distance, cam_distance*0.75, -cam_distance))
        # cam.location = center + Vector((cam_distance, cam_distance*0.75, cam_distance))
        # cam.location = center + Vector((-cam_distance, cam_distance*0.75, cam_distance))
        # cam.location = center + Vector((-cam_distance, cam_distance*0.75, -cam_distance))
        direction = center - cam.location


        # cam.location = location

        # cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        # set rotation only
        set_cam_attributes_explicity(cam, direction, up=Vector((0, 1, 0)))  # 手动控制 up 向量为 -X 或任意方向
        



    # === 设置背景为白色 ===
    bpy.context.scene.world.use_nodes = True
    bg = bpy.context.scene.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # === 渲染设置 ===
    bpy.context.scene.render.engine = 'CYCLES'                # 使用 Cycles 渲染器（真实光影）
    bpy.context.scene.render.filepath = get_output_path()           # 设置输出路径
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.cycles.samples = 64                     # 设置采样数量（影响画质和速度）

# === 开始渲染并保存图片 ===
bpy.ops.render.render(write_still=True)


# blender --background --python .\blender\render_overlap.py 


# 1. 打开 Blender
# 2. 切换到 Scripting 标签页
# 3. 选择此文件
# 4. 点击 Run Script 按钮


# TODO: 封装成函数

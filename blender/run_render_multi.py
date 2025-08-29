# run_render_multi.py
import subprocess
import os

# blend_script = "E:/SIGGRAPH-GS-ColorVis/blender/render_multi.py"
blend_script = "./blender/render_multi.py"

model_name1 = "trex"  # 模型名称
model_name2 = "lego"  # 模型名称
model_name3 = "hook"  # 模型名称
model_name4 = "jump"  # 模型名称
ply_paths = [
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name1}_PLY/ours_{model_name1}_1.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name1}_PLY/ours_{model_name1}_2.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name1}_PLY/ours_{model_name1}_3.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name1}_PLY/ours_{model_name1}_4.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name1}_PLY/motion_{model_name1}_1.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name1}_PLY/motion_{model_name1}_2.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name1}_PLY/motion_{model_name1}_3.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name1}_PLY/motion_{model_name1}_4.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name1}_PLY/seg_{model_name1}_1.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name1}_PLY/seg_{model_name1}_2.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name1}_PLY/seg_{model_name1}_3.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name1}_PLY/seg_{model_name1}_4.ply",    
    
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name2}_PLY/ours_{model_name2}_1.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name2}_PLY/ours_{model_name2}_2.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name2}_PLY/ours_{model_name2}_3.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name2}_PLY/ours_{model_name2}_4.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name2}_PLY/motion_{model_name2}_1.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name2}_PLY/motion_{model_name2}_2.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name2}_PLY/motion_{model_name2}_3.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name2}_PLY/motion_{model_name2}_4.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name2}_PLY/seg_{model_name2}_1.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name2}_PLY/seg_{model_name2}_2.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name2}_PLY/seg_{model_name2}_3.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name2}_PLY/seg_{model_name2}_4.ply",    

    f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name3}_PLY/ours_{model_name3}_1.ply",
    f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name3}_PLY/ours_{model_name3}_2.ply",
    f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name3}_PLY/ours_{model_name3}_3.ply",
    f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name3}_PLY/ours_{model_name3}_4.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name3}_PLY/motion_{model_name3}_1.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name3}_PLY/motion_{model_name3}_2.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name3}_PLY/motion_{model_name3}_3.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name3}_PLY/motion_{model_name3}_4.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name3}_PLY/seg_{model_name3}_1.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name3}_PLY/seg_{model_name3}_2.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name3}_PLY/seg_{model_name3}_3.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name3}_PLY/seg_{model_name3}_4.ply",    
    
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name4}_PLY/ours_{model_name4}_1.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name4}_PLY/ours_{model_name4}_2.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name4}_PLY/ours_{model_name4}_3.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name4}_PLY/ours_{model_name4}_4.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name4}_PLY/motion_{model_name4}_1.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name4}_PLY/motion_{model_name4}_2.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name4}_PLY/motion_{model_name4}_3.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name4}_PLY/motion_{model_name4}_4.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name4}_PLY/seg_{model_name4}_1.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name4}_PLY/seg_{model_name4}_2.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name4}_PLY/seg_{model_name4}_3.ply",
    # f"E:/SIGGRAPH-GS-ColorVis/ply/{model_name4}_PLY/seg_{model_name4}_4.ply",    
]
seg_keys = ['seg_id_l1', 'seg_id_l2', 'seg_id_l3', 'seg_id_l4']
    

for i, ply_path in enumerate(ply_paths):
    if i <= 1:
        continue
    # # # #
    k = i % 12
    gaussian_on = "True" if k < 4 else "False"
    seg_key = seg_keys[k % 4]

    print(f"Rendering: {ply_path} | seg_key={seg_key} | GAUSSIAN_ON={gaussian_on}")

    subprocess.run([
        "blender", "--background", "--python", blend_script, "--",
        ply_path, seg_key, gaussian_on
    ])


# 运行脚本
# python ./blender/run_render_multi.py
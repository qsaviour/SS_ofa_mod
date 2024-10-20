import bpy
import random

# 随机设置人物摄像机的follow path的起止点

objects =[
    "Camera_close_1-1_Char",
    "Camera_close_1-2_Char",
    "Camera_close_1-3_Char",
    "Camera_norm_1-1_Char",

    "Camera_close_2-1_Char",
    "Camera_close_2-2_Char",
    "Camera_close_2-3_Char",
    "Camera_norm_2-1_Char",

    "Camera_close_3-1_Char",
    "Camera_close_3-2_Char",
    "Camera_close_3-3_Char",
    "Camera_norm_3-1_Char",

    # "Camera_close_4-1_Char",
    # "Camera_close_4-2_Char",
    # "Camera_close_4-3_Char",
    # "Camera_norm_4-1_Char",

    # "Camera_close_5-1_Char",
    # "Camera_close_5-2_Char",
    # "Camera_close_5-3_Char",
    # "Camera_norm_5-1_Char",
]

current_area = bpy.context.area.type

for ind,obj_name in enumerate(objects):
    
    obj = bpy.data.objects[obj_name]
    follow_path = obj.constraints['Follow Path']
    
    frame_start = bpy.context.scene.frame_start
    frame_end = bpy.context.scene.frame_end
    value = random.randint(0,100)
    sign = -1 if ind%2 else 1
    keyframes = {
        frame_start: value,    # 在帧1，偏移为0.0
        frame_end : value + sign * (200 + random.randint(-30,30))
    }
    for frame, offset in keyframes.items():
        bpy.context.scene.frame_set(frame)
        follow_path.offset = offset
        follow_path.keyframe_insert(data_path="offset", frame=frame)

        # 确保当前帧设置为初始帧
    bpy.context.scene.frame_set(1)

    # 获取动画数据和F曲线
    fcurves = obj.animation_data.action.fcurves

    # 遍历所有F曲线并设置插值类型为线性
    for fcurve in fcurves:
        if fcurve.data_path == 'constraints["Follow Path"].offset':
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = 'LINEAR'
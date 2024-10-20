import bpy

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

if bpy.context.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

for ind,obj_name in enumerate(objects):
    
    obj = bpy.data.objects.get(obj_name)
    # if obj is None:
    #     continue
    # obj.location = (0.0, 0.0, 0.0)
    # obj.rotation_euler = (0.0, 0.0, 0.0)

    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

start_frame = bpy.context.scene.frame_start
end_frame = bpy.context.scene.frame_end
bpy.context.scene.frame_set(start_frame)

# 手动烘焙 》》》》》》》》》
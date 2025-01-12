import bpy

objects =[
    "Camera_close_1-1_Char",
    "Camera_close_1-2_Char",
    "Camera_close_1-3_Char",
    "Camera_norm_1-1_Char",
    "Camera_close_1-3_Char_pan",
    "Camera_close_1-3_Char_pan_long",
    "Camera_close_1-3_Char_h_pan",
    "Camera_close_1-3_Char_ass",
    
    "Camera_close_2-1_Char",
    "Camera_close_2-2_Char",
    "Camera_close_2-3_Char",
    "Camera_norm_2-1_Char",
    "Camera_close_2-3_Char_pan",
    "Camera_close_2-3_Char_pan_long",
    "Camera_close_2-3_Char_h_pan",
    "Camera_close_2-3_Char_ass",

    "Camera_close_3-1_Char",
    "Camera_close_3-2_Char",
    "Camera_close_3-3_Char",
    "Camera_norm_3-1_Char",
    "Camera_close_3-3_Char_pan",
    "Camera_close_3-3_Char_pan_long",
    "Camera_close_3-3_Char_h_pan",
    "Camera_close_3-3_Char_ass",

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
    if obj_name not in bpy.data.objects:
        print(obj_name,"not found!!!")
        continue
    obj = bpy.data.objects.get(obj_name)

    if obj and obj.constraints:
        for constraint in obj.constraints:
            constraint.mute = False  # 或者 False，视情况而定

    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

start_frame = bpy.context.scene.frame_start
end_frame = bpy.context.scene.frame_end
bpy.context.scene.frame_set(start_frame)


# init position
# bake animation >>

import bpy

objects = [
    ["Camera_close_1-1_Char",5],
    ["Camera_close_1-2_Char",5],
    ["Camera_norm_1-1_Char",10],

    ["Camera_close_2-1_Char",5],
    ["Camera_close_2-2_Char",5],
    ["Camera_norm_2-1_Char",10],

    ["Camera_close_3-1_Char",5],
    ["Camera_close_3-2_Char",5],
    ["Camera_norm_3-1_Char",10],

    ["Camera_close_4-1_Char",5],
    ["Camera_close_4-2_Char",5],
    ["Camera_norm_4-1_Char",10],
    
    ["Camera_close_5-1_Char",5],
    ["Camera_close_5-2_Char",5],
    ["Camera_norm_5-1_Char",10],
]    
current_area = bpy.context.area.type
for obj_name,times in objects:
    
    obj = bpy.data.objects[obj_name]
    
    if obj.animation_data and obj.animation_data.action:
        
        action = obj.animation_data.action
        
        for fcurve in action.fcurves:
            if len(fcurve.keyframe_points)<=2:
                continue
            for keyframe in fcurve.keyframe_points:
                keyframe.select_control_point = True
        
        obj.update_tag(refresh = {"DATA"})
        
    for xx in range(times):
        
        bpy.context.area.type = "GRAPH_EDITOR"
        bpy.ops.graph.smooth()
#        bpy.ops.graph.smooth()

bpy.context.area.type = current_area
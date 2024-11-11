import bpy
import tqdm
import mathutils 

# 指定你的骨骼对象名称和骨骼名称
armature_name = "Armature"
source_bone_name = "AO_Base"
target_bone_name = "Root"

# 获取骨骼对象
armature = bpy.data.objects[armature_name]

# 进入姿态模式
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')

# 获取骨骼姿态
source_bone = armature.pose.bones[source_bone_name]
target_bone = armature.pose.bones[target_bone_name]

frame_start = bpy.context.scene.frame_start
frame_end = bpy.context.scene.frame_end


for frame in tqdm.tqdm(range(frame_start, frame_end + 1)):
    bpy.context.scene.frame_set(frame)
    if frame == 0:
        target_off = target_bone.location
        tf = [e for e in target_off]
        source_bone.location+=mathutils.Vector((-tf[2],tf[1],tf[0]))
        target_bone.location-=target_off
    else:
        source_bone.location+=mathutils.Vector((-tf[2],tf[1],tf[0]))
    l = source_bone.location

    target_bone.location = (l[2],l[1],-l[0])
    source_bone.location = (0,0,0)

    target_bone.keyframe_insert(data_path="location", frame=frame)
    source_bone.keyframe_insert(data_path="location", frame=frame)

    if frame >100:
        break
import bpy
import tqdm
import mathutils 

def fix_armatures(armature_name):

    # 指定你的骨骼对象名称和骨骼名称
    # armature_name = "Armature"
    base_bone_name = "AO_Base"
    root_bone_name = "Root"

    # 获取骨骼对象
    armature = bpy.data.objects[armature_name]

    # 进入姿态模式
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    # 获取骨骼姿态
    base_bone = armature.pose.bones[base_bone_name]
    root_bone = armature.pose.bones[root_bone_name]

    frame_start = bpy.context.scene.frame_start
    frame_end = bpy.context.scene.frame_end


    for frame in tqdm.tqdm(range(frame_start, frame_end + 1)):
        bpy.context.scene.frame_set(frame)
        if frame == 0:
            root_off = root_bone.location
            tf = [e for e in root_off]
            root_bone.location-=mathutils.Vector((tf[0],0,tf[2]))
            base_bone.location+=mathutils.Vector((-tf[2],0,tf[0]))
        else:
            base_bone.location+=mathutils.Vector((-tf[2],0,tf[0]))
        
        root_off = root_bone.location
        tf = [e for e in root_off]
        root_bone.location-=mathutils.Vector((0,tf[1],0))
        base_bone.location+=mathutils.Vector((0,tf[1],0))

        l = base_bone.location
        rl = root_bone.location
        root_bone.location = (l[2],rl[1],-l[0])
        base_bone.location = (0,l[1],0)

        root_bone.keyframe_insert(data_path="location", frame=frame)
        base_bone.keyframe_insert(data_path="location", frame=frame)

        # if frame >100:
        #     break

for an in ['Armature','CharArmature2','CharArmature3','CharArmature4','CharArmature5']:
    fix_armatures(an)
# for an in ['CharArmature1','CharArmature2','CharArmature3']:
#     fix_armatures(an)

# for an in ['CharArmature1']:
#     fix_armatures(an)
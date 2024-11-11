import bpy
import bmesh
import tqdm

# - 215

armature_and_meshs = [
    ('Armature','SK_chr_body_base'),
    ('Armature.001','SK_chr_body_base.001'),
    ('Armature.002','SK_chr_body_base.002'),
    ('Armature.003','SK_chr_body_base.003'),
    ('Armature.004','SK_chr_body_base.004'),
    ('Armature.005','SK_chr_body_base.005'),
    ('Armature.006','SK_chr_body_base.006'),
]

def get_lowest_point(obj):
    bm = bmesh.new()
    bm.from_object(obj, bpy.context.evaluated_depsgraph_get())
    vertex_positions = [obj.matrix_world @ vertex.co for vertex in bm.verts]
    lowest_point = min(vertex_positions, key=lambda v: v.z)
    return lowest_point

def fix_height(armature_name,object_name):
# 指定你的骨骼对象名称和骨骼名称
    bone_name = "AO_Base"

    # 获取骨骼对象
    armature = bpy.data.objects[armature_name]
    obj = bpy.data.objects[object_name]

    # 进入姿态模式
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    # 获取骨骼姿态
    base_bone = armature.pose.bones[bone_name]

    frame_start = bpy.context.scene.frame_start
    frame_end = bpy.context.scene.frame_end

    # lowest_points_init =None
    lowest_points_init = 0
    for frame in tqdm.tqdm(range(frame_start,frame_end+1)):
        bpy.context.scene.frame_set(frame)
        lowest_point = get_lowest_point(obj)

        base_bone.location.y += max(0,lowest_points_init-lowest_point.z)
        base_bone.keyframe_insert(data_path="location", frame=frame)

for a,o in armature_and_meshs:
    fix_height(a,o)
    
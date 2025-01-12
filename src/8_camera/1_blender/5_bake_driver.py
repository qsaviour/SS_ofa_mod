import bpy
import math
import tqdm

objects =[
    ["CameraNormal_1","cam_dan_cng_cam3_u1out.ao","Camera_fov"],
    ["CameraNormal_3","cam_dan_cng_cam3_u3out.ao","Camera_fov"],
    # ["CameraNormal_5","cam_dan_cng_cam3_u5out.ao","Camera_fov"],
]

def bake_driver(objs):
    camera_name,armature_name,bone_name = objs

    camera = bpy.data.objects[camera_name]
    camera = bpy.data.cameras[camera.data.name]
    if camera.animation_data.action:
        for fcurve in camera.animation_data.action.fcurves:
            if fcurve.data_path == "lens":
                camera.animation_data.action.fcurves.remove(fcurve)
    camera = bpy.data.objects[camera_name]

    armature = bpy.data.objects.get(armature_name)
    pose_bone = armature.pose.bones.get(bone_name)
    
    scene = bpy.context.scene
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    for frame in tqdm.tqdm(range(start_frame, end_frame + 1)):
        scene.frame_set(frame)
        rotation_quaternion = pose_bone.rotation_quaternion.x
        camera.data.lens = (30 / 2) / math.tan(math.radians(-rotation_quaternion*170/ 2))
        camera.data.keyframe_insert(data_path='lens',frame= frame)

for obj in objects:
    bake_driver(obj)
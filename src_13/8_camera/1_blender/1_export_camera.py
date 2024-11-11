import bpy
import math
import tqdm
import json

def export_camera():
    # camera_name = "CameraNormal_1"

    # camera = bpy.data.objects[camera_name]
    # camera = bpy.data.cameras[camera.data.name]
    # camera = bpy.data.objects[camera_name]

#    scene = bpy.context.scene
#    # 获取当前活动摄像机
#    camera = scene.camera

    camera_name = "CameraNormal_1.001"
    camera = bpy.data.objects[camera_name]
    
    scene = bpy.context.scene
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    results = []
    for frame in tqdm.tqdm(range(start_frame, end_frame + 1)):
        scene.frame_set(frame)
        x,y,z = camera.location
        a,b,c = camera.matrix_world.to_euler()
        fl = camera.data.lens
        res = [ x,y,z,a,b,c,fl]
        results.append(res)
    path = r'F:\IMModels\ModProject\Dance\Scripts\cache_target\env\live13_camera\dumped.json'
    f = open(path,'w')
    json.dump(results,f)

export_camera()
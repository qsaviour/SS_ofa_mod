import bpy
import tqdm
import json

def get_or_create_main_camera():
    main_camera = bpy.data.objects.get("MainCamera")
    if main_camera is None:
        bpy.ops.object.camera_add()
        main_camera = bpy.context.active_object
        main_camera.name = "MainCamera"
    return main_camera

def switch_camera_properties(main_camera, target_camera):
    main_camera.location = target_camera.location
    main_camera.rotation_euler = target_camera.rotation_euler
    main_camera.data.lens = target_camera.data.lens

def integrate_cameras():
    main_camera = get_or_create_main_camera()

    scene = bpy.context.scene
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    jump_frames = []

    all_marksers = list(scene.timeline_markers)
    # print([e.camera for e in all_marksers])

    for frame in tqdm.tqdm(range(start_frame, end_frame + 1)):
        scene.frame_set(frame)
        if all_marksers and frame >= all_marksers[0].frame:
            active_camera = all_marksers[0].camera
            all_marksers = all_marksers[1:]
            if frame>0:
                jump_frames.append(frame-1)
        # if active_camera!=last_camera:
        #     jump_frames.append(frame)
        
        main_camera.location = active_camera.matrix_world.translation
        main_camera.rotation_euler = active_camera.matrix_world.to_euler()
        main_camera.data.lens = active_camera.data.lens
        main_camera.keyframe_insert(data_path="location", frame=frame)
        main_camera.keyframe_insert(data_path="rotation_euler", frame=frame)
        main_camera.data.keyframe_insert(data_path="lens", frame=frame)
    with open(r'F:\IMModels\ModProject\Dance\Scripts\cache_target\camera\merged_camera.json','w') as f:
        json.dump(jump_frames,f)
    print(jump_frames)
        

integrate_cameras()
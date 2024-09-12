import unreal

level_sequence_paths = [
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Num1_Camera.LS_Sng026_Num1_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Num2_Camera.LS_Sng026_Num2_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Num3_Camera.LS_Sng026_Num3_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Num4_Camera.LS_Sng026_Num4_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Common_Camera.LS_Sng026_Common_Camera',

    '/Game/Sequence/Live/Sng026/LS_Sng026_Large_Num1_Camera.LS_Sng026_Large_Num1_Camera',
    '/Game/Sequence/Live/Sng026/LS_Sng026_Large_Num2_Camera.LS_Sng026_Large_Num2_Camera',
    '/Game/Sequence/Live/Sng026/LS_Sng026_Large_Num3_Camera.LS_Sng026_Large_Num3_Camera',
    '/Game/Sequence/Live/Sng026/LS_Sng026_Large_Num4_Camera.LS_Sng026_Large_Num4_Camera',
    '/Game/Sequence/Live/Sng026/LS_Sng026_Large_Num5_Camera.LS_Sng026_Large_Num5_Camera',

    # '/Game/Sequence/Live/Sng026/LS_Sng026_Middle_Num1_Camera.LS_Sng026_Middle_Num1_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Middle_Num2_Camera.LS_Sng026_Middle_Num2_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Middle_Num3_Camera.LS_Sng026_Middle_Num3_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Middle_Num4_Camera.LS_Sng026_Middle_Num4_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Middle_Num5_Camera.LS_Sng026_Middle_Num5_Camera',

    # '/Game/Sequence/Live/Sng026/LS_Sng026_Small_Num1_Camera.LS_Sng026_Small_Num1_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Small_Num2_Camera.LS_Sng026_Small_Num2_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Small_Num3_Camera.LS_Sng026_Small_Num3_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Small_Num4_Camera.LS_Sng026_Small_Num4_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Small_Num5_Camera.LS_Sng026_Small_Num5_Camera',
]

def deal_level_sequence(level_sequence_path):
    print("!!! Processing :",level_sequence_path)
    level_sequence = unreal.load_asset(level_sequence_path)
    # 获取或创建 Camera Cut Track
    camera_cut_track = level_sequence.find_master_tracks_by_type(unreal.MovieSceneCameraCutTrack)

    for camera_track in camera_cut_track:
        Sections = camera_track.get_sections()
        for section in Sections:                    
            camera_track.remove_section(section)

    stacks = {}
    bindings = level_sequence.get_bindings()
    for binding in bindings:
        if 'Cine Camera Actor' not in str(binding.get_display_name()):
            continue
        for track in binding.get_tracks():
            for section in track.get_sections():
                for channel in section.get_channels():
                    keys = channel.get_keys()
                    stack = []
                    for key in keys:
                        frame,value = key.get_time().frame_number.value,key.get_value()
                        stack.append(frame)
                    if stack:
                        start_frames = [stack[0]]+ [b for a,b in zip(stack[:-1],stack[1:]) if a!=b-1]
                        end_frames = [a for a,b in zip(stack[:-1],stack[1:]) if a!=b-1] + [stack[-1]]
                        stacks[str(binding.get_display_name())] = [start_frames,end_frames,binding]

    for start_frames,end_frames,binding in stacks.values():
        for start_frame,end_frame in zip(start_frames,end_frames):
            section = camera_track.add_section()
            section.set_range(start_frame,end_frame+1)
            # property = section.get_editor_property('CameraBindingID')
            # property.set_editor_property('Guid',binding.get_id())
            # # camera_binding_object_binding_id = unreal.MovieSceneObjectBindingID()
            # # camera_binding_object_binding_id.set_editor_property('Guid', binding.get_id())
            # # section.set_editor_property('CameraBindingID', camera_binding_object_binding_id)
for level_sequence_path in level_sequence_paths:
    deal_level_sequence(level_sequence_path)
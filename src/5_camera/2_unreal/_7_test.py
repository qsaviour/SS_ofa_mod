import unreal

level_sequence_paths = [
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Num1_Camera.LS_Sng026_Num1_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Num2_Camera.LS_Sng026_Num2_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Num3_Camera.LS_Sng026_Num3_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Num4_Camera.LS_Sng026_Num4_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Common_Camera.LS_Sng026_Common_Camera',

    # '/Game/Sequence/Live/Sng026/LS_Sng026_Large_Num1_Camera.LS_Sng026_Large_Num1_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Large_Num2_Camera.LS_Sng026_Large_Num2_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Large_Num3_Camera.LS_Sng026_Large_Num3_Camera',
    # '/Game/Sequence/Live/Sng026/LS_Sng026_Large_Num4_Camera.LS_Sng026_Large_Num4_Camera',
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

    bindings = level_sequence.get_bindings()
    # for binding in bindings:
    #     print("****",str(binding.get_display_name()),binding.get_id(),binding.get_parent().get_id())
        # raise
        

    # stacks = {}
    # bindings = level_sequence.get_bindings()
    # for binding in bindings:
    #     if 'Cine Camera Actor' not in str(binding.get_display_name()):
    #         continue
    #     for track in binding.get_tracks():
    #         for section in track.get_sections():
    #             for channel in section.get_channels():
    #                 keys = channel.get_keys()
    #                 stack = []
    #                 for key in keys:
    #                     frame,value = key.get_time().frame_number.value,key.get_value()
    #                     stack.append(frame)
    #                 if stack:
    #                     start_frames = [stack[0]]+ [b for a,b in zip(stack[:-1],stack[1:]) if a!=b-1]
    #                     end_frames = [a for a,b in zip(stack[:-1],stack[1:]) if a!=b-1] + [stack[-1]]
    #                     stacks[str(binding.get_display_name())] = [start_frames,end_frames,binding,section]

    # for start_frames,end_frames,biding,section in stacks.values():
    #     try:
    #         print("****",section.get_editor_property('CameraBindingID'),str(section.get_editor_property('CameraBindingID')),binding.get_id(),binding.get_parent().get_id())
    #     except:
    #         pass

    bindings = level_sequence.get_bindings()
    # for binding in bindings:
    #     if 'Cine Camera Actor' not in str(binding.get_display_name()):
    #         continue
    for track in camera_cut_track:
        print("!!! New Track")
        for section in track.get_sections():
            try:
                property_ = section.get_editor_property('CameraBindingID')
                guid = property_.get_editor_property("Guid")
                print("****",section,property_,guid)
            except Exception as e:
                print(section,e)


for level_sequence_path in level_sequence_paths:
    deal_level_sequence(level_sequence_path)
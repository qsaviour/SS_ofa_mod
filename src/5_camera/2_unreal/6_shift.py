import unreal

level_sequence_paths = [
    # '/Game/Sequence/Live/cam_1.cam_1',
    # '/Game/Sequence/Live/cam_2.cam_2',
    # '/Game/Sequence/Live/cam_3.cam_3',
    # '/Game/Sequence/Live/cam_4.cam_4',
    '/Game/Sequence/Live/cam_5.cam_5',
]

OFFSET = -180

def shift_level_sequence(level_sequence_path,offset = OFFSET):
    level_sequence = unreal.load_asset(level_sequence_path)
    bindings = level_sequence.get_bindings()
    for binding in bindings:
        print(binding.get_display_name())
        for track in binding.get_tracks():
            for section in track.get_sections():
                for channel in section.get_channels():
                    keys = channel.get_keys()
                    stack = []
                    for key in keys:
                        frame,value = key.get_time().frame_number.value,key.get_value()
                        stack.append((frame,value))
                    for key in keys:
                        channel.remove_key(key)
                    for frame,value in stack:
                        new_key = channel.add_key(time = unreal.FrameNumber(frame+OFFSET),new_value = value)

for level_sequence_path in level_sequence_paths:
    shift_level_sequence(level_sequence_path)

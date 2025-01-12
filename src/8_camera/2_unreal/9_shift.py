import unreal

level_sequence_paths = [
    '/Game/Sequence/Live/camM.camM'
]
OFFSET = -180

def shift_level_sequence(level_sequence_path,offset = OFFSET):
    level_sequence = unreal.load_asset(level_sequence_path)
    bindings = level_sequence.get_bindings()
    for binding in bindings:
        for track in binding.get_tracks():
            for section in track.get_sections():
                for channel in section.get_channels():
                    keys = channel.get_keys()
                    for key in keys:
                        current_time = key.get_time()
                        new_time = unreal.FrameNumber(current_time.frame_number.value + offset)
                        key.set_time(new_time)

for level_sequence_path in level_sequence_paths:
    shift_level_sequence(level_sequence_path)

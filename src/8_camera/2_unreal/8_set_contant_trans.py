import unreal
import json
import re
# from pathlib import Path


with open(r'F:\IMModels\ModProject\Dance\Scripts\cache_target\camera\merged_camera.json') as f:
    jump_frames = json.load(f)

level_sequence_path = '/Game/Sequence/Live/camM.camM'
# level_sequence_path = '/Game/Sequence/Live/Sng026/LS_Sng026_Common_Camera.LS_Sng026_Common_Camera'
# level_sequence_path = '/Game/Sequence/Live/Sng026/NewLevelSequence.NewLevelSequence'
level_sequence = unreal.load_asset(level_sequence_path)

print("^^^^^^^^^^^^")
for i,binding in enumerate(level_sequence.get_bindings()):
    tracks = binding.get_tracks()
    for track in tracks:
        for section in track.get_sections():
            for channel in section.get_channels():
                print("##",binding.get_name(),str(track.get_display_name()))
                if str(track.get_display_name()) in {"Transform","Current Focal Length"}:
                    keys = channel.get_keys()
                    for key in keys:
                        time = key.get_time()
                        cur_frame = int(time.frame_number.value)
                        if cur_frame in jump_frames:
                            # print(key.get_interpolation_mode(),dir(unreal.RichCurveInterpMode))
                            key.set_interpolation_mode(unreal.RichCurveInterpMode.RCIM_CONSTANT)



import unreal
import json
import re
# from pathlib import Path


ofa_root =  r"f:\IMModels\ModProject\Dance\Song_col"
ofa_cache = ofa_root + '/cache'
with open(ofa_cache+'/camera'+'/camera_res.json') as f:
    ofa_data = json.load(f)

level_sequence_path = "/Game/Sequence/Live/Sng026/LS_Sng026_Common_Chara.LS_Sng026_Common_Chara"
# level_sequence_path = '/Game/Sequence/Live/Sng026/LS_Sng026_Common_Camera.LS_Sng026_Common_Camera'
# level_sequence_path = '/Game/Sequence/Live/Sng026/NewLevelSequence.NewLevelSequence'
level_sequence = unreal.load_asset(level_sequence_path)


for i,binding in enumerate(level_sequence.get_bindings()):
    if "BP_LiveCharacter" not in binding.get_name():
        continue
    ss_look_at = ofa_data["camera_look_cam"]
    tracks = binding.get_tracks()
    for track in tracks:
        if track.get_property_name()=="bLookAtOn":
            for section in track.get_sections():
                for channel in section.get_channels():
                    keys = channel.get_keys()
                    for key in keys:
                        channel.remove_key(key)
                    for new_key in ss_look_at:
                        frame,if_look_at = new_key
                        channel.add_key(time=unreal.FrameNumber(frame),new_value=if_look_at)


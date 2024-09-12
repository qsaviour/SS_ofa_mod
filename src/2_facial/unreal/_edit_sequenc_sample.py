import unreal
import json

# ss_file = json.load(r"E:\IMModels\ModProject\Dance\Song_Col\facial\ss\facial.json")

# 定义 Level Sequence 的路径
level_sequence_path = "/Game/Sequence/Live/Sng026/LS_Sng026_Common_Chara.LS_Sng026_Common_Chara"
# level_sequence_path = '/Game/Sequence/Live/Sng026/LS_Sng026_Common_Camera.LS_Sng026_Common_Camera'
# level_sequence_path = '/Game/Sequence/Live/Sng026/NewLevelSequence.NewLevelSequence'
level_sequence = unreal.load_asset(level_sequence_path)

for i,binding in enumerate(level_sequence.get_bindings()):
    tracks = binding.get_tracks()
    obj = tracks[0]
    for track in tracks:
        print(track.get_property_name())
        for section in track.get_sections():
            for channel in section.get_channels():
                keys = channel.get_keys()
                for key in keys:
                    channel.remove_key(key)
                new_key = channel.add_key(time=unreal.FrameNumber(10),new_value=10)
        break
    break


import unreal
import json
import re

ss_data = json.load(open(r"E:\IMModels\ModProject\Dance\Song_ful\cache\facial\facial.json"))


ss_data = {int(k):v for k,v in ss_data.items()}
# 定义 Level Sequence 的路径
level_sequence_path = "/Game/Sequence/Live/Sng026/LS_Sng026_Common_Chara.LS_Sng026_Common_Chara"
# level_sequence_path = '/Game/Sequence/Live/Sng026/LS_Sng026_Common_Camera.LS_Sng026_Common_Camera'
# level_sequence_path = '/Game/Sequence/Live/Sng026/NewLevelSequence.NewLevelSequence'
level_sequence = unreal.load_asset(level_sequence_path)


for i,binding in enumerate(level_sequence.get_bindings()):
    if "BP_LiveCharacter" not in binding.get_name():
        continue
    c_ind = ord(binding.get_name()[-1])-ord('A')
    print(binding.get_name(),c_ind)
    ss_faces = ss_data[c_ind]
    tracks = binding.get_tracks()
    for track in tracks:
        if track.get_property_name()=="FacialID":
            for section in track.get_sections():
                for channel in section.get_channels():
                    keys = channel.get_keys()
                    for key in keys:
                        channel.remove_key(key)
                    for new_key in ss_faces:
                        frame,face_id,is_closed,force_closed = new_key
                        channel.add_key(time=unreal.FrameNumber(frame),new_value=face_id)
        elif track.get_property_name()=="bForceCloseEyes":
            for section in track.get_sections():
                for channel in section.get_channels():
                    keys = channel.get_keys()
                    for key in keys:
                        channel.remove_key(key)
                    for new_key in ss_faces:
                        frame,face_id,is_closed,force_closed = new_key
                        if not is_closed and force_closed:
                            channel.add_key(time=unreal.FrameNumber(frame),new_value=True)
                        else:
                            channel.add_key(time=unreal.FrameNumber(frame),new_value=False)
    #     break
    # break


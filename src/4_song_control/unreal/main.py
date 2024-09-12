import json
import unreal

bpm,control_datas = json.load(open(r'E:\IMModels\ModProject\Dance\Scripts\src\4_song_control\unreal\control_data.json'))
ss_control_path = '/Game/Sequence/Live/Sng026/LS_Sng026_Common_Chara.LS_Sng026_Common_Chara'

level_sequence = unreal.EditorAssetLibrary.load_asset(ss_control_path)
bindings = level_sequence.get_bindings()
for binding in bindings:
    # print(binding.get_display_name())
    if binding.get_display_name() == 'LiveSingingController':
        for track in binding.get_tracks():
            n = int(str(track.get_property_name())[-3]) -1
            print(track.get_property_name(),"!!!!",n)
            for section in track.get_sections():
                for channel in section.get_channels():
                    keys = channel.get_keys()
                    for key in keys:
                        channel.remove_key(key)
                    control_data = [(e[n],e[-1]) for e in control_datas]
                    for value,beat in control_data:
                        frame = int(beat*1.0/bpm*60*60)
                        mark = bool(value)
                        print("!!!",beat,value,mark,bpm)
                        new_key = channel.add_key(time=unreal.FrameNumber(frame),new_value=mark)
                # break
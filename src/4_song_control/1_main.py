from pathlib import Path
from parse_xml import parse_ofa_song_control
import json

info_folder_path = Path(r'E:\IMModels\ModProject\Dance\Song_bnd\info')

info_file = info_folder_path/'info.txt'
ts2_file = list(info_folder_path.glob('ts2*.xml'))[0] ; print(ts2_file)
bpm = open(info_file).read().split('\n')[0]

control_data = parse_ofa_song_control(ts2_file)
print(control_data)

control_data = [int(bpm),control_data]

json.dump(control_data,open('unreal/control_data.json','w'))

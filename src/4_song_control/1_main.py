from pathlib import Path
from parse_xml import parse_ofa_song_control
import json

root_ = json.load(open('../root_folder.json'))['root']

Test_Root = Path(root_)

info_folder_path = Test_Root/'info'

info_file = info_folder_path/'info.txt'
ts2_file = list(info_folder_path.glob('ts2*.xml'))[0] ; print(ts2_file)
bpm = open(info_file).read().split('\n')[0]

control_data = parse_ofa_song_control(ts2_file)
print(control_data)

control_data = [int(bpm),control_data]

target_file = Test_Root/'cache/song_control/control_data.json'
target_file.parent.mkdir(exist_ok=True,parents=True)
json.dump(control_data,open(target_file,'w'))
print(f"done! Write to {target_file}")

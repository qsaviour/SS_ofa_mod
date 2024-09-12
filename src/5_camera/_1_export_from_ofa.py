from pathlib import Path
from lxml import etree
import json
import random
random.seed(768)
from collections import defaultdict

ofa_root =  Path(r"e:\IMModels\ModProject\Dance\Song_Col")
ofa_ts = ofa_root / "info/ts2_col.xmb.xml"
ofa_cache = ofa_root/'cache'
ofa_cache.mkdir(exist_ok=True,parents=True)

info_file_path = ofa_root/'info'/'info.txt'
ofa_bpm = int(open(info_file_path).read().split()[0])

def parse_ofa(path,bpm):
    tree = etree.parse(path)
    root = tree.getroot()
    data = {}
    data['camera_pattern_id_map'] = {}
    data['camera_beat'] = []
    data['camera_ids'] = []
    for e in root:
        if e.attrib['class']=='TimingSheetEnv':
            for camera_pattern_data in e:
                if camera_pattern_data.attrib['class'] == "CameraPattern":
                    for camera_pattern in camera_pattern_data:
                        pattern_no = int(camera_pattern.attrib['pattern_id'])
                        for stage in camera_pattern:
                            res = [0]*4
                            res_id,res_value = 0,0
                            for prob in stage:
                                camera_id = int(prob.attrib['camera_id'])
                                value = int(prob.attrib['value'])
                                res[camera_id] = value
                                if value>=res_value:
                                    res_id,res_value = camera_id,value
                            data['camera_pattern_id_map'][pattern_no] = res_id
                            break
        if e.attrib['class']=='CameraController':
            for event in e:
                beat = float(event.attrib['beat'])
                frame = round(beat/bpm*60*60)
                camera_pattern = int(event.attrib['camera_id'])
                data['camera_beat'].append((frame,camera_pattern))
    for frame,camera_pattern in data['camera_beat']:
        camera_id = data['camera_pattern_id_map'][camera_pattern]
        data['camera_ids'].append((frame,camera_id))
    data.pop('camera_pattern_id_map')
    data.pop('camera_beat')
    return data


o_data = parse_ofa(ofa_ts,ofa_bpm)
res = defaultdict(list)
for char_num in range(5):
    res[char_num].append([-214,3,30]) # 添加初始摄像头
    for frame,value in o_data['camera_ids']:
        if value in {0,1}:
            camera = random.randint(1,char_num+1)
            if value == 0:
                fov = random.randint(35,45)
            elif value == 1:
                fov = random.randint(30,35)
        elif value == 2:
            camera = -1
            fov = 30
        elif value == 3:
            camera = -2
            fov = random.randint(25,30)
        else:
            raise 
        res[char_num].append([frame,camera,fov])


# with open(ofa_cache/'camera_beat.json','w') as f:
#     json.dump(data,f)

with open(ofa_cache/'camera_res.json','w') as f:
    json.dump(res,f)
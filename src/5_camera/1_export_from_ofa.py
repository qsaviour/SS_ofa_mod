from pathlib import Path
from lxml import etree
import json
import random
random.seed(768)
from collections import defaultdict

ofa_root =  Path(r"e:\IMModels\ModProject\Dance\Song_Cng")
ofa_ts = ofa_root / "info/ts2_cng.xmb_new.xml"
ofa_cache = ofa_root/'cache'/'camera'
ofa_cache.mkdir(exist_ok=True,parents=True)

info_file_path = ofa_root/'info'/'info.txt'
ofa_bpm = open(info_file_path).read().split()[0]

def parse_ofa(path,bpm):
    tree = etree.parse(path)
    root = tree.getroot()
    data = {}
    data['camera_pattern_id_map'] = {}
    data['camera_beat'] = []
    data['camera_ids'] = [[0,2]]
    data['camera_target'] = [[0,0]]
    data['camera_look_cam'] = [[0,0]]
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
                frame = round(beat*60*60/bpm)
                camera_pattern = int(event.attrib['camera_id'])
                data['camera_beat'].append((frame,camera_pattern))

                data['camera_target'].append((frame,int(event.attrib['target'])))
                data['camera_look_cam'].append((frame,int(event.attrib['look_cam'])))
    for frame,camera_pattern in data['camera_beat']:
        camera_id = data['camera_pattern_id_map'][camera_pattern]
        data['camera_ids'].append((frame,camera_id))
    data.pop('camera_pattern_id_map')
    data.pop('camera_beat')
    return data

res = parse_ofa(ofa_ts,ofa_bpm)

with open(ofa_cache/'camera_res.json','w') as f:
    json.dump(res,f)
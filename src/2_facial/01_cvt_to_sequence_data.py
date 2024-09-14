from pathlib import Path
from lxml import etree
import json
import re
from collections import Counter
import random
random.seed(768)

Test_Root = Path(r'E:\IMModels\ModProject\Dance\Song_bnd')

info_folder = Test_Root/"info"
info_file_name = info_folder/"info.txt"
xml_file = list(info_folder.glob('*ts2*.xml'))[0]
ss_face_target_file = Test_Root/"facial"/"ss"/"facial.json"

ofa_ss_face_id_map = json.load(open(r"E:\IMModels\ModProject\Dance\Scripts\src\2_facial\ofa_ss_face_Id_map.json"))
ofa_ss_face_id_map = {int(k):v for k,v in ofa_ss_face_id_map.items()}
# tree = etree.parse(xml_file)
# root = tree.getroot()

bpm = int(open(info_file_name).readlines()[0])

tree = etree.parse(xml_file)
root = tree.getroot()

face_pattern_id_map = {}
for layer1 in root:
    if layer1.attrib['class']=='TimingSheetEnv':
        for layer2 in layer1:
            if layer2.attrib['class'] == 'FacePattern':
                for layer3 in layer2:
                    face_pattern_id = layer3.attrib['pattern_id']

                    faces = [e.attrib for e in layer3]
                    face_ids = [int(e['face_id']) for e in faces if e['face_id']]
                    if len(face_ids)==0:
                        continue
                    face_id = Counter(face_ids).most_common()[0][0]
                    is_closeds = [bool(e['eye']) for e in faces]
                    is_closed = Counter(is_closeds).most_common()[0][0]

                    face_pattern_id_map[int(face_pattern_id)] = (face_id,is_closed)

res = {}
for layer1 in root:
    if not layer1.attrib.has_key('name'):
        continue
    rm =  re.findall("face_\w*_(\d+)",layer1.attrib['name'])
    if rm:
        ind = int(rm[0])
        res[ind]= [[0,0,0,0]]
        for layer2 in layer1:
            data = layer2.attrib
            beat = data['beat']
            if not beat:
                continue
            frame = round(float(beat)/float(bpm)*60*60)
            face_pattern = data['face_id']
            face_id,force_closed = face_pattern_id_map[int(face_pattern)]
            if face_id not in ofa_ss_face_id_map:
                print(f"FaceID: {face_id} not known. Frame: {frame}. Beat: {beat}. character: {layer2.attrib['character_no']}",)
            else:
                ss_face_id,is_closed = ofa_ss_face_id_map[face_id][:2]
                res[ind].append([frame,ss_face_id,is_closed,force_closed])

# add random blink
#10-30帧眨眼 60-90帧间隔
cur_frame = 0
cur_closed = True
for k,v in res.items():
    new_v = []
    for ind,((a1,a2,a3,a4),(b1,b2,b3,b4)) in enumerate(zip(v[:-1],v[1:])):
        new_v.append([a1,a2,a3,a4])
        if not a3 and not a4:
            if cur_closed:
                cur_frame = a1
            cur_closed = False
            gap = random.randint(60,120)
            while cur_frame<b1-gap:
                gap = random.randint(60,350)
                dur = random.randint(13,30)
                if cur_frame+gap+dur+20>b1:
                    break
                v1 = [cur_frame+gap,a2,a3,True]
                v2 = [cur_frame+gap+dur,a2,a3,False]
                new_v.append(v1)
                new_v.append(v2)
                cur_frame += gap+dur
                gap = random.randint(60,120)
        else:
            cur_closed = True

    new_v.append([b1,b2,b3,b4])
    res[k] = new_v

ss_face_target_file.parent.mkdir(exist_ok=True,parents=True)
with open(ss_face_target_file,'w') as f:
    json.dump(res,f)

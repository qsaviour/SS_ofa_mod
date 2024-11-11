from pathlib import Path
import json
from lxml import etree
import random
from env_map import name_color_map,horizon_map
from file_map import file_map
random.seed(768)

BEAT_OFFSET = 0.5

root_ = json.load(open('../root_folder.json'))['root']

root_folder = Path(root_)

info_folder = root_folder/'info'
ts1_file = next(info_folder.glob('ts1*.xml'))
info_file = info_folder/'info.txt'

target_folder = root_folder/'cache/env/ofa_env.json'

def cvt_color(color_n,smooth_color = None,reverse=True):
    
    if type(color_n) == str:
        color_n = int(color_n)
    h = hex(color_n)
    if len(h)==6:
        h = h[2:]+'00'
    elif color_n == 0:
        h = '0'*6
    else:
        h = h[2:]
    a,b,c = h[:2],h[2:4],h[4:6]
    a,b,c = map(lambda z:int(z,16)/255,(a,b,c))
    if smooth_color is not None:
        sa,sb,sc = smooth_color
        a,b,c = (a+sa)/2,(b+sb)/2,(c+sc)/2
    if reverse:
        return c,b,a
    return a,b,c

def enhance_color(color,mixed_color = (0.5,0.5,0.5),weight=0.8):
    a,b,c = color
    aa,bb,cc = mixed_color
    return [(a+weight*aa)/(weight+1),(b+weight*bb)/(weight+1),(c+weight*cc)/(weight+1)]

def parse_stage_color(pnode,file_id_color_map):
    bpm = int(open(info_file).read().split()[0])
    stack = []
    first_empty_node = False
    # seen_frame = set()
    for node in pnode:
        beat,fade_time,file_id = [(node.attrib[key]) for key in ['beat','fade_time','LTRFile_id']]
        if not beat and first_empty_node:
            continue
        if not beat:
            first_empty_node = True
        frame = (float(beat)+BEAT_OFFSET)*60*60/bpm if beat else -180
        color_name,brightness,individuallyRatio = file_id_color_map[file_id]
        color = random.choice(name_color_map[color_name])
        color = enhance_color(color)
        fade_time = float(fade_time)
        if fade_time:
            fade_frame = frame+fade_time*60*60/bpm
            last_res = {k:v for k,v in stack[-1].items()}
            last_res["frame"],last_res["is_fade"] = frame,True
            stack.append(last_res)
            frame = fade_frame
        res = {'frame':frame,'color':color,'color_name':color_name,'brightness':brightness,'individuallyRatio':individuallyRatio,'is_fade':False}
        stack.append(res)
    return stack

def parse_fade_frame(pnode):
    bpm = int(open(info_file).read().split()[0])
    fade_beat = 0
    for node in pnode:
        if node.attrib['beat']:
            fade_beat = float(node.attrib['beat'])+BEAT_OFFSET
    frame = fade_beat*60*60/bpm
    return frame

def parse_fade_datas(pnode,keys=[],fade_key = "color_time"):
    bpm = int(open(info_file).read().split()[0])
    datas = []
    first_empty_node = False
    for node in pnode:
        if not node.attrib['beat']:
            if not first_empty_node:
                frame = -180
            else:
                continue
        else:
            beat = float(node.attrib['beat'])+BEAT_OFFSET
            first_empty_node = True
            frame = int(beat*60*60/bpm)
        if fade_key in node.attrib and datas and float(node.attrib[fade_key])>0:
            fade_time = float(node.attrib[fade_key])
            fade_frame = frame+fade_time*60*60/bpm
            last_res = {k:v for k,v in datas[-1].items()}
            last_res["frame"],last_res["is_fade"] = frame,True
            datas.append(last_res)
            frame = fade_frame

        color = cvt_color(node.attrib['color'])
        color = enhance_color(color)
        data = {'frame':frame,'color':color,'is_fade':False}
        for key in keys:
            if key in node.attrib:
                data[key] = node.attrib[key]
        datas.append(data)
    return datas

def parse_datas(pnode,keys = []):
    bpm = int(open(info_file).read().split()[0])
    datas = []
    for node in pnode:
        if not node.attrib['beat']:
            continue
        beat = float(node.attrib['beat'])+BEAT_OFFSET
        frame = int(beat*60*60/bpm)
        color = cvt_color(node.attrib['color'])
        color = enhance_color(color)
        data = {'frame':frame,'color':color}
        for key in keys:
            if key in node.attrib:
                data[key] = node.attrib[key]
        datas.append(data)
    return datas


def export_ofa_env():
    
    tree = etree.parse(ts1_file)
    env_root = tree.getroot()
    bpm = int(open(info_file).read().split()[0])

    file_id_color_map = {}
    file_id_tsk_map = {}
    all_stack = {}
    all_stack['bpm'] = bpm
    

    for l1 in env_root:
        if l1.tag == 'file':
            name = l1.attrib['name']
            if '.ltr' in name:
                name = name.split('.')[0]
                if 'win' in name or 'lose' in name:
                    continue
                
                color,brightness,indiviuallyRatio = file_map[name]
                file_id_color_map[l1.attrib['file_id']] = color,brightness,indiviuallyRatio
            elif '.tsk' in name and 'horizon' in name:
                name = name.split('.')[0].split('_')[-1]
                if name == 'horizonoff':
                    num=-1
                else:
                    obj,num = name[:-2],int(name[-2:])
                file_id_tsk_map[l1.attrib['file_id'] ] = num

    for l1 in env_root:
        if "class" in l1.attrib and l1.attrib['class'] == "StageColorController" and l1.attrib['name'] == "pos_eff_stage_in":
            all_stack['stage_color'] = parse_stage_color(l1,file_id_color_map)
        elif 'class' in l1.attrib and l1.attrib['class'] == "SoftFocusController" and l1.attrib['name'] == "pos_eff_softfocus_in":
            all_stack['fade_frame'] = parse_fade_frame(l1)
        elif 'class' in l1.attrib and l1.attrib['class'] == "SpotlightController" and 'pos_eff_light' in l1.attrib['name']:
            all_stack['spot_light'] = all_stack.get('spot_light',{})
            num = int(l1.attrib['name'][-2:])
            all_stack['spot_light'][num] = all_stack['spot_light'].get(num)
            all_stack['spot_light'][num]=parse_fade_datas(l1,['alpha'])
        elif 'class' in l1.attrib and l1.attrib['class'] == "EffectEventController" and 'laser' in l1.attrib['name']:
            all_stack['laser_light'] = all_stack.get('laser_light',{})
            num = int(l1.attrib['name'][-2:])
            all_stack['laser_light'][num] = all_stack['laser_light'].get(num)
            all_stack['laser_light'][num] = parse_datas(l1,['action'])
        elif 'class' in l1.attrib and l1.attrib['class'] == "SpotlightController" and 'fixlight' in l1.attrib['name']:
            all_stack['fix_light'] = all_stack.get('fix_light',{})
            num = int(l1.attrib['name'][-2:])
            all_stack['fix_light'][num] = all_stack['fix_light'].get(num)
            all_stack['fix_light'][num] = parse_fade_datas(l1,['alpha'])
        elif 'class' in l1.attrib and l1.attrib['class'] == "SpotlightController" and 'serchlight' in l1.attrib['name']:
            all_stack['serch_light'] = all_stack.get('serch_light',{})
            num = int(l1.attrib['name'][-2:])
            all_stack['serch_light'][num] = all_stack['serch_light'].get(num)
            all_stack['serch_light'][num] = parse_fade_datas(l1,['alpha'])
        elif 'class' in l1.attrib and l1.attrib['class'] == "SpotlightController" and 'menlaser' in l1.attrib['name']:
            all_stack['menlaser_light'] = all_stack.get('menlaser_light',{})
            num = int(l1.attrib['name'][-2:])
            all_stack['menlaser_light'][num] = all_stack['menlaser_light'].get(num)
            all_stack['menlaser_light'][num] = parse_datas(l1)
        elif 'class' in l1.attrib and l1.attrib['class'] == "SpotlightController" and 'olaser' in l1.attrib['name']:
            all_stack['olaser_light'] = all_stack.get('olaser_light',{})
            num = int(l1.attrib['name'][-2:])
            all_stack['olaser_light'][num] = all_stack['olaser_light'].get(num)
            all_stack['olaser_light'][num] = parse_datas(l1)
        elif 'class' in l1.attrib and l1.attrib['class'] == "EffectEventController" and l1.attrib['name'] == "pos_eff_pfall01":
            all_stack['paper_fall']=parse_datas(l1)
        elif 'class' in l1.attrib and l1.attrib['class'] == "EffectEventController" and l1.attrib['name'] == "pos_eff_canon01":
            all_stack['canon']=parse_datas(l1)
        elif 'class' in l1.attrib and l1.attrib['class'] == "EffectEventController" and l1.attrib['name'] == "pos_eff_gus01":
            all_stack['gus']=parse_datas(l1)
        elif 'class' in l1.attrib and l1.attrib['class'] == "EffectEventController" and l1.attrib['name'] == "pos_eff_smoke01":
            all_stack['smoke']=parse_datas(l1)
        elif 'class' in l1.attrib and l1.attrib['class'] == "EffectEventController" and l1.attrib['name'] == "pos_eff_horiz01":
            all_stack['horizon']=parse_datas(l1,['EffectFile_id','play_speed'])
            for e in all_stack['horizon']:
                e['EffectFile_id'] = horizon_map[file_id_tsk_map[e['EffectFile_id']]]
                

        elif 'class' in l1.attrib and l1.attrib['class'] == "LightMapCharaController" and l1.attrib['name'] == "pos_eff_lightmap_chara_out":
            all_stack['decal?']=parse_datas(l1,['LMapCharaTex_id'])
    
    
    target_folder.parent.mkdir(exist_ok=True,parents=True)
    with open(target_folder,'w',encoding='utf-8') as f:
        json.dump(all_stack,f)
    print(f"Save To {target_folder}")
export_ofa_env()
import bpy
from pathlib import Path
import json
import random
from collections import Counter

TOTAL_CHAR_NUM = 3

FRAME_DELAY = 180 + 15

ofa_root =  Path(r"f:\IMModels\ModProject\Dance\Song_gmw")
ofa_cache = ofa_root/'cache'
with open(ofa_cache/'camera'/'camera_res.json') as f:
    ofa_data = json.load(f)

BASE_FOCAL_LENGTH = 45
FOCAL_NOISE = 3

CamerasPatter1 = {
            1:{
                'close':['Camera_close_1-1_Char',"Camera_close_1-2_Char","Camera_close_1-3_Char",],
                'norm':["Camera_norm_1-1_Char"],
            },
            2:{
                'close':['Camera_close_2-1_Char',"Camera_close_2-2_Char","Camera_close_2-3_Char",],
                'norm':["Camera_norm_2-1_Char"],
            },
            3:{
                'close':['Camera_close_3-1_Char',"Camera_close_3-2_Char","Camera_close_3-3_Char",],
                'norm':["Camera_norm_3-1_Char"],
            },
            4:{
                'close':['Camera_close_4-1_Char',"Camera_close_4-2_Char","Camera_close_4-3_Char",],
                'norm':["Camera_norm_4-1_Char"],
            },
            5:{
                'close':['Camera_close_5-1_Char',"Camera_close_5-2_Char","Camera_close_5-3_Char",],
                'norm':["Camera_norm_5-1_Char"],
            },
}

CamerasPatter2 = {
            1:{'close':["Camera_close_1-1_Char","Camera_close_1-2_Char","Camera_close_1-3_Char",],
                'norm':["Camera_norm_1-1_Char"]},
            2:{'close':["Camera_close_2-1_Char","Camera_close_2-2_Char","Camera_close_2-3_Char",],
                'norm':["Camera_norm_2-1_Char"]},
            3:{'close':["Camera_close_3-1_Char","Camera_close_3-2_Char","Camera_close_3-3_Char",],
                'norm':["Camera_norm_3-1_Char"]},
            4:{'close':["Camera_close_4-1_Char","Camera_close_4-2_Char","Camera_close_4-3_Char",],
                'norm':["Camera_norm_4-1_Char"]},
            5:{'close':["Camera_close_5-1_Char","Camera_close_5-2_Char","Camera_close_5-3_Char",],
                'norm':["Camera_norm_5-1_Char"]},
            'auto':{ # total_num
                1:["CameraNormal_1"],
                2:["CameraNormal_3"],
                3:["CameraNormal_3"],
                4:["CameraNormal_5"],
                5:["CameraNormal_5"],
            },
            'long':["CameraLong"]
        }

def clear_focal(camera_name):
    if camera_name not in bpy.data.objects:
        return
    camera = bpy.data.objects[camera_name]
    camera = bpy.data.cameras[camera.data.name]
    if camera.animation_data.action:
        for fcurve in camera.animation_data.action.fcurves:
            if fcurve.data_path == "lens":
                camera.animation_data.action.fcurves.remove(fcurve)

char_mark_map = {
    5:{1:1,2:2,3:3,6:1,7:1},
    4:{1:1,2:2,3:3,6:2,7:3},
    3:{1:1,2:2,3:3,6:1,7:1},
    2:{1:1,2:2,3:3,6:3,7:2},
    1:{2:1,3:1,6:1,7:1}
}
char_choise_able={
    5:[1,2,3,4,5],
    4:[2,3,4,5],
    3:[1,2,3],
    2:[2,3],
    1:[1]
}

class Char_Getter():
    def __init__(self,total_char_num):
        self.total_char_num = total_char_num
        self.cameras = CamerasPatter1
        for _,v in self.cameras.items():
            for _,camera_names in v.items():
                for camera_name in camera_names:
                    clear_focal(camera_name)
        self.counter = Counter()
        for _,target in ofa_data['camera_target']:
            if target != 0:
                target = char_mark_map[self.total_char_num][target]
                self.counter[target]+=1

    
    def get_char_by_mark(self,mark,last_char):
        print(self.counter)
        if mark == 0:
            bac_chars = char_choise_able[self.total_char_num]
            counter = self.counter.copy()
            if last_char is not None:
                counter.pop(last_char)
            most_common_count = list(counter.most_common())[-1][-1]
            bac_chars = [e[0] for e in counter.items() if e[1] == most_common_count]
            char = random.choice(bac_chars)
        else:
            char = char_mark_map[self.total_char_num][mark]
        self.counter[char] +=1
        return char

class CameraGetter():
    def __init__(self,total_char_num):
        self.cameras=CamerasPatter2
        self.seen_cameras = set()
        self.char_getter = Char_Getter(total_char_num)
        self.last_char = None
    def get_camera_by_mark(self,camera_mark,char_mark):
        char = None
        if camera_mark == 0: # close camera
            char = self.char_getter.get_char_by_mark(char_mark,self.last_char)
            bac_cameras = self.cameras[char]['close']
            focal_length = BASE_FOCAL_LENGTH + random.randint(-FOCAL_NOISE,FOCAL_NOISE)
        elif camera_mark == 1: # norm camera
            char = self.char_getter.get_char_by_mark(char_mark,self.last_char)
            bac_cameras = self.cameras[char]['norm']
            focal_length = BASE_FOCAL_LENGTH + random.randint(-FOCAL_NOISE,FOCAL_NOISE)
        elif camera_mark == 2: # auto camera
            # char = self.char_getter.get_char_by_mark(char_mark)
            bac_cameras = self.cameras['auto'][self.char_getter.total_char_num]
            focal_length = None
        else:
            bac_cameras = self.cameras['long']
            focal_length = None
            # print(type(char_mark))
            # raise ValueError(f"camera_mark-{camera_mark} not in [0,1,2]")
        if char is not None:
            self.last_char = char
        if all([e in self.seen_cameras for e in bac_cameras]):
            for e in bac_cameras:
                self.seen_cameras.remove(e)
        bac_cameras = [e for e in bac_cameras if e not in self.seen_cameras]
        camera = random.choice(bac_cameras)
        self.seen_cameras.add(camera)

        return camera,focal_length

print(ofa_data)
# raise NotImplementedError

camera_getter = CameraGetter(TOTAL_CHAR_NUM)

scene = bpy.context.scene
scene.timeline_markers.clear()

for ind in range(len(ofa_data['camera_ids'])-1,-1,-1):
    if ofa_data['camera_ids'][ind][-1]==0:
        if ofa_data['camera_target'][ind][-1]==0:
            ofa_data['camera_target'][ind][-1] = 6
            break

for ind,((frame,camera_mark),(_,char_mark)) in enumerate(zip(ofa_data['camera_ids'],ofa_data['camera_target'])):
    if frame !=0 :
        frame += FRAME_DELAY
    
    camera_name,focal_length = camera_getter.get_camera_by_mark(camera_mark,char_mark)
    camera = bpy.data.objects[camera_name]
    
    if frame !=0 and camera_mark!=2: # not auto camera
        camera.data.keyframe_insert(data_path='lens',frame= frame-1)
        if focal_length is not None:
            camera.data.lens = focal_length
        camera.data.keyframe_insert(data_path='lens',frame= frame)
    marker1 = scene.timeline_markers.new(f'F_{frame}', frame=frame)
    marker1.camera = camera
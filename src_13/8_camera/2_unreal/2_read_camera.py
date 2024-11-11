import unreal
import json
import re
import math

camera_file = open(r"F:\IMModels\ModProject\Dance\Scripts\cache_target\env\live13_camera\dumped.json")

camera_binding_name = "CameraNormal_1"
camera_data = json.load(camera_file)

level_sequence_path = '/Game/Sequence/Live/Sng029/LS_Sng029_Common_Camera.LS_Sng029_Common_Camera'
OFFSET = -180
DIS = 10

def is_loc_jump(camera_data,frame):
    if frame+1 < len(camera_data):
        x,y,z = camera_data[frame][:3]
        nx,ny,nz = camera_data[frame+1][:3]
        if abs(nx-x)>DIS or abs(ny-y)>DIS or abs(nz-z)>DIS:
            return True
    return False

level_sequence = unreal.load_asset(level_sequence_path)
bindings = level_sequence.get_bindings()
for binding in bindings:
    for track in binding.get_tracks():
        try: # remove focal length
            if str(track.get_property_name())=="Current Focal Length":
                for section in track.get_sections():
                    for channel in section.get_channels():
                        keys = channel.get_keys()
                        for key in keys:
                            channel.remove_key(key)
                        for frame in range(len(camera_data)):
                            value = camera_data[frame][6]-5
                            if is_loc_jump(camera_data,frame):
                                channel.add_key(time = unreal.FrameNumber(frame + OFFSET),new_value = value,interpolation=unreal.MovieSceneKeyInterpolation.CONSTANT)
                            else:
                                channel.add_key(time = unreal.FrameNumber(frame + OFFSET),new_value = value)
        except Exception as e:
            print("ERROR!~!!",e)

name_map={
    "Location.X":0,
    "Location.Y":1,
    "Location.Z":2,
    "Rotation.X":4,
    "Rotation.Y":3,
    "Rotation.Z":5,
}


for binding in bindings:
    for track in binding.get_tracks():      
        for section in track.get_sections():
            for channel in section.get_channels():
                name = str(channel.get_name())
                if name in name_map:
                    keys = channel.get_keys()
                    for key in keys:
                        channel.remove_key(key)
                    ind = name_map[name]
                    for frame in range(len(camera_data)):
                        value = camera_data[frame][ind]
                        if "Rotation" in name:
                            value = math.degrees(value)
                        if name == "Location.Y":
                            value = -value

                        # if name == "Rotation.Y":
                        #     value = -value
                        if name == "Rotation.Y":
                            value = value-90
                        elif name == "Rotation.Z":
                            value = -value-90
                        
                        if is_loc_jump(camera_data,frame):
                            channel.add_key(time = unreal.FrameNumber(frame + OFFSET),new_value = value,interpolation=unreal.MovieSceneKeyInterpolation.CONSTANT)
                        else:
                            channel.add_key(time = unreal.FrameNumber(frame + OFFSET),new_value = value)
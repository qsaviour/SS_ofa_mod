from pathlib import Path
import os
import json
from ofa_lip import parse_ofa
from ss_lip import cvt_ss

root_ = json.load(open('../root_folder.json'))['root']

Test_Root = Path(root_)

ofa_folder = Test_Root/'lip'/'ofa'
ofa_file_name = list(ofa_folder.glob('*.lip'))[0]

def open_ss_file(ss_lip_file):
    with open(ss_lip_file) as f:
        data =json.load(f)
    return data
def save_ss_data(ss_data,target_ss_lip_file:Path):
    target_ss_lip_file.parent.mkdir(exist_ok=True,parents=True)
    with open(target_ss_lip_file,'w') as f:
        json.dump(ss_data,f, indent=2, ensure_ascii=False)

def convert_lip(root:Path,ss_file_name,ofa_file_name):
    lip_folder = root/"lip"
    ofa_lip_folder = lip_folder/"ofa"
    target_ss_file = root/'cache'/'lip'/(ss_file_name+'_ofa_target')

    ofa_lip_file = ofa_lip_folder/ofa_file_name
    ofa_data = parse_ofa(ofa_lip_file)

    target_ss_data = cvt_ss(ofa_data)
    save_ss_data(target_ss_data,target_ss_file)
    print("save to",target_ss_file)
    # data['Exports'][0]['Data'][0]['Value'][i]['Value][0]['Value'][face_ind]['Value']
    pass


ss_file_name ="LipSync_Sng026_00" 
convert_lip(Test_Root,ss_file_name,ofa_file_name)
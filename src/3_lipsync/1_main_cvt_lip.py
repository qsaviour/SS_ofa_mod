from pathlib import Path
import os
import json
from ofa_lip import parse_ofa
from ss_lip import cvt_ss

def open_ss_file(ss_lip_file):
    with open(ss_lip_file) as f:
        data =json.load(f)
    return data
def save_ss_data(ss_data,target_ss_lip_file):
    with open(target_ss_lip_file,'w') as f:
        json.dump(ss_data,f, indent=2, ensure_ascii=False)

def convert_lip(root:Path,ss_file_name,ofa_file_name):
    lip_folder = root/"lip"
    ofa_lip_folder = lip_folder/"ofa"
    ss_lip_folder = lip_folder/"ss"
    ss_target_lip_folder = lip_folder/"Song026"
    ss_target_lip_folder.mkdir(exist_ok=True)

    # ss_lip_file = ss_lip_folder/ss_file_name
    target_ss_file = ss_lip_folder/(ss_file_name+'_ofa_target')
    # ss_data = open_ss_file(ss_lip_file)


    ofa_lip_file = ofa_lip_folder/ofa_file_name
    ofa_data = parse_ofa(ofa_lip_file)

    target_ss_data = cvt_ss(ofa_data)
    save_ss_data(target_ss_data,target_ss_file)
    # data['Exports'][0]['Data'][0]['Value'][i]['Value][0]['Value'][face_ind]['Value']
    pass


if __name__ == '__main__':
    # 把ofa数据准备成可以用uassetapi处理的数据
    Test_Root = Path(r'E:\IMModels\ModProject\Dance\Song_Cng')
    ss_file_name ="LipSync_Sng026_00" 
    ofa_file_name = "lipsync_cng.lip"
    convert_lip(Test_Root,ss_file_name,ofa_file_name)
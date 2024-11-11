from pathlib import Path
import subprocess
import sys
import os
import time
import json
import shutil

# Test_Root = Path(r'E:\IMModels\ModProject\Dance\Song_meg')
Test_Root = Path(json.load(open('../root_folder.json'))['root'])

def convert_sons(root):
    HCA = "4ee10a3e3bb19e57"

    with open('character_map.json') as f:
        name_map = json.load(f)

    o_work_dir = Path(os.curdir).absolute()
    song_folder = root/"song"
    ofa_song_folder = song_folder/"ofa"
    ss_song_folder = song_folder/"ss"
    ss_target_sonf_folder = song_folder/"Song026"
    if not ss_target_sonf_folder.exists():
        ss_target_sonf_folder.mkdir()

    def convert_song(ue_file,ofa_file):
        with open(ue_file,'rb') as f:
            data = f.read()
        ind = data.index(b'AFS2')
        data_new = data[ind:]
        subkey = data_new[14:16].hex()
        
        with open("tmp.awb",'wb') as f:
            f.write(data_new)
        subprocess.run(['awb2hcas.bat','tmp.awb'],input=b'\n')
        os.chdir('tmp')
        source_hca = Path('./1.hca')
        subprocess.run(["vgmstream.exe",f"{ofa_file}"])
        wav_file = ofa_file.parent/(ofa_file.name+".wav")
        if '_bgm' in wav_file.name:
            subprocess.run(['ffmpeg','-i',f"{wav_file}",'-af','volume=1.1','output.wav','-y']) # -i input.mp4 -af "volume=2.0" output.mp4
        else:
            subprocess.run(['ffmpeg','-i',f"{wav_file}",'-af','volume=1.2','output.wav','-y']) # -i input.mp4 -af "volume=2.0" output.mp4
        os.remove(wav_file)
        shutil.move('output.wav',f"{wav_file}")
        p=subprocess.run(["hcaenc.exe",f"{wav_file}"])
        hca_file = wav_file.parent/wav_file.name.replace(".wav",".hca")

        with open(source_hca,'rb') as sf:
            source_hca_length = len(sf.read())
        with open(hca_file,'rb') as tf:
            data = tf.read()
        assert source_hca_length > len(data)
        data = data + b'0'*(source_hca_length - len(data))
        hca_file_1 = hca_file.parent/(hca_file.name+'_1')
        hca_file_2 = hca_file.parent/(hca_file.name+'_2')
        with open(hca_file_1,'wb') as tf:
            tf.write(data)
        os.chdir(hca_file_1.parent)
        subprocess.run(["hcacc",hca_file_1.name,hca_file_2.name,
                        "-o1",f"{HCA[8:]}","-o2",f"{HCA[:8]}",
                        "-om",f"{subkey[2:]}{subkey[:2]}","-ot","56"])
        with open(hca_file_2,'rb') as tf:
            cvt_data = tf.read()
        cvt_data = cvt_data +  b'0'*(source_hca_length - len(cvt_data))

        with open(ue_file,'rb') as sf:
            s_data = sf.read()
        ind = s_data.find(b"\xC8\xC3\xC1")
        new_s_data = s_data[:ind] + cvt_data + s_data[ind+len(cvt_data):]
        with open(ss_target_sonf_folder/ue_file.name,'wb') as tf:
            tf.write(new_s_data)
        os.chdir(o_work_dir)
        return ss_target_sonf_folder/ue_file.name

    for ofa_file in ofa_song_folder.glob('*.nus3bank'):
        s_name = ofa_file.name.split('.')[0][-3:]
        t_name = name_map[s_name][0]
        ue_file = ss_song_folder/f"CueSheet_SWAV_Sng021_{t_name}.uexp"
        # print(ue_file,ue_file.exists())
        out_file = convert_song(ue_file,ofa_file)
        for c_name in name_map[s_name][1:]:
            # c_file = ss_song_folder/f"CueSheet_SWAV_Sng026_{c_name}.uexp"
            shutil.copy(out_file,ss_target_sonf_folder/f"CueSheet_SWAV_Sng021_{c_name}.uexp")

    ue_p_folder = song_folder/'Audio/CueSheet/Song/Song021'
    ue_p_folder.mkdir(parents=True,exist_ok=True)
    shutil.rmtree(ue_p_folder,ignore_errors=True)
    shutil.move(ss_target_sonf_folder,ue_p_folder)

convert_sons(Test_Root)
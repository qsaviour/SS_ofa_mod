
# data['Exports'][0]['Data'][0]['Value'][i]['Value'][0]['Value'][face_ind]['Value']
import tqdm
ss_lip_map_c = {
    "A":10,
    "a":6,
    "I":12,
    "O":13,
    "E":11,
    "U":14
}
ss_lip_map_i = {
    1:(10,1),
    2:(10,0.3),
    3:(12,1),
    4:(13,1),
    5:(11,1),
    6:(14,1),
}


def cvt_ss(ofa_data):
    ss_datas = []
    for i in tqdm.tqdm(range(len(ofa_data))):
        ss_data = [0.0]*16
        for j,jj in ss_lip_map_i.items():
            ss_data[jj[0]]+=ofa_data[i][j]*jj[1]
        ss_datas.append(ss_data)
    return ss_datas
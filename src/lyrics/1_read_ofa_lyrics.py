from pathlib import Path
from lxml import etree

root_folder = Path(r'E:\IMModels\ModProject\Dance\Song_Col')

info_folder = root_folder/'info'
sheet_file = root_folder/'info'/'ts2_col.xmb.xml' ####
info_file = root_folder/'info'/'info.txt'

bmp = int(open(info_file).read().split()[0])


lyric_folder = root_folder/'lyrics'
ofa_folder = lyric_folder/'ofa'
ss_folder = lyric_folder/'ss'

info_file = ofa_folder
lyric_id_file = ofa_folder/'lyrics_col.xmb.xml'

tree = etree.parse(lyric_id_file)
root = tree.getroot()
lyric_id_map = {}
for e in root:
    lyric_id = e.attrib['id']
    assert len(list(e))==1
    for ee in e:
        lyric_text = ee.attrib['_text']
    lyric_id_map[lyric_id] = lyric_text
    raise NotImplementedError

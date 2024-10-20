from pathlib import Path
import json
from lxml import etree

root_ = json.load(open('../root_folder.json'))['root']

root_folder = Path(root_)

info_folder = root_folder/'info'
lyrics_folder = root_folder/'lyrics'
info_file = info_folder/'info.txt'
ts2_file = next(info_folder.glob('*ts2*.xml'))
lyrics_file = next(lyrics_folder.glob('lyrics*.xml'))

def parse_lyrics():
    tree = etree.parse(lyrics_file)
    lyric_root = tree.getroot()
    lyric_id_text_map = {}
    for e in lyric_root:
        lyric_id = e.attrib['id'].split('_')[1]
        lyric_id = int(lyric_id)
        for ee in e:
            lyric = ee.attrib['_text']
            lyric = lyric.replace('\u3000',' ')
            lyric_id_text_map[lyric_id] = lyric
    return lyric_id_text_map

def parse_lyric_control(lyric_id_text_map):
    bpm = int(open(info_file).read().split()[0])
    tree = etree.parse(ts2_file)
    ts2_root = tree.getroot()
    lyrics = []
    for l1 in ts2_root:
        if l1.attrib['class'] == "LyricsController":
            for l2 in l1:
                beat,lyric_id,action = l2.attrib["beat"],l2.attrib["lyric_no"],l2.attrib["action"]
                beat, lyric_id,action = float(beat),int(lyric_id),int(action)
                start_time = beat*60/bpm
                if (lyric_id == 0 or action == -1):
                    if lyrics:
                        lyrics[-1][1] = start_time
                else:
                    lyric = lyric_id_text_map[lyric_id]
                    lyrics.append([start_time,None,lyric])
    for i in range(len((lyrics))):
        lyric = lyrics[i]
        if lyric[1] is None:
            lyrics[i][1] = lyrics[i+1][0]
    return lyrics


def export_lyrics():
    
    lyric_id_text_map = parse_lyrics()
    lyrics = parse_lyric_control(lyric_id_text_map)
    target = root_folder/"cache\lyrics\lyrics.json"
    target.parent.mkdir(exist_ok=True,parents=True)
    with open(target,'w',encoding='utf-8') as f:
        json.dump(lyrics,f,ensure_ascii=False)
    print(f'done! write to {target}')

export_lyrics()
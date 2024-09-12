from lxml import etree
import unreal

def parse_ofa_song_control(xml_file):
    tree = etree.parse(xml_file)
    root = tree.getroot()
    ress = []
    for child1 in root:
        if child1.attrib['class'] == 'SongPartController':
            for child2 in child1:
                r = {k:v for k,v in child2.attrib.items()}
                res = [r['mv01'],r['sv01'],r['sv02'],r['sv03'],r['sv04']]
                res = list(map(int,res))
                res = res + [float(r['beat'])]
                ress.append(res)
    return ress

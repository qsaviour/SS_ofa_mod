import struct
from pathlib import Path
from collections import Counter
from xml.etree import ElementTree
import json

root = Path(json.load(open('../root_folder.json'))['root'])/"info"

final_counter = Counter()

class Entry:
    size = 16
    def __init__(self,index,bytes) -> None:
        self.index = index
        self.bytes = bytes
        self.name_offset,bytes = read_slice(bytes,4,'int')
        self.attribute_count,bytes = read_slice(bytes,2,'ushort')
        self.child_count,bytes = read_slice(bytes,2,'ushort')
        bytes_ = bytes
        self.attribute_start_index,bytes = read_slice(bytes,2,'short')
        if self.attribute_start_index < 0 :
            self.attribute_start_index,bytes = read_slice(bytes_,2,'ushort')
        self.unk1,bytes = read_slice(bytes,2)
        self.parent_index,bytes = read_slice(bytes,2,'short')
        self.unk2,bytes = read_slice(bytes,2)
        self.name = None
        self.attributes = []
    def __repr__(self) -> str:
        return f"E{self.index}|{self.attribute_start_index}|{self.attribute_count}"

class Attribute:
    size = 8
    def __init__(self,index,bytes) -> None:
        self.index = index
        self.bytes = bytes
        self.name_offset,bytes = read_slice(bytes,4,'int')
        self.value_offset,bytes = read_slice(bytes,4,'int')
        self.name = None
        self.value = None
    def __repr__(self) -> str:
        return f"A{self.index}|{self.name_offset}|{self.value_offset}|{self.name}|{self.value}"
class MappedEntry:
    size = 8
    def __init__(self,index,bytes) -> None:
        self.index = index
        self.bytes = bytes
        self.value_offset,bytes = read_slice(bytes,4,'int')
        self.entry_index,bytes = read_slice(bytes,4,'int')
    def __repr__(self) -> str:
        return f"ME{self.index}|{self.value_offset}|{self.entry_index}"
    
def read_slice(data,length,as_type = None,start=0):
    res:bytes = data[start:start+length]
    data = data[start+length:]
    if as_type is None:
        pass
    elif as_type =='str':
        res.decode()
    elif as_type=='int':
        res = struct.unpack('>I',res)[0]
    elif as_type=='ushort':
        res = struct.unpack('>H',res)[0]
    elif as_type=='short':
        res = struct.unpack('>h',res)[0]
    return res,data

def parse_entries(entries_bytes):
    entries = []
    for ii,i in enumerate(range(0,len(entries_bytes),Entry.size)):
        entries.append(Entry(ii,entries_bytes[i:i+Entry.size]))
    return entries
def parse_attributes(attributes_bytes):
    attributes = []
    for ii,i in enumerate(range(0,len(attributes_bytes),Attribute.size)):
        attributes.append(Attribute(ii,attributes_bytes[i:i+Attribute.size])) 
    return attributes
def parse_mapped_entries(mapped_entry_bytes):
    mapped_entries = []
    for ii,i in enumerate(range(0,len(mapped_entry_bytes),MappedEntry.size)):
        mapped_entries.append(MappedEntry(ii,mapped_entry_bytes[i:i+MappedEntry.size]))
    return mapped_entries

def cut_value(bytes,start):
    seg = bytes[start:]
    end_ind = seg.index(b'\x00') if seg else 0
    seg = seg[:end_ind]
    return decode(seg)

def decode(b):
    try:
        return b.decode('utf-8')
    except:
        s = []
        for i in range(0,len(b),2):
            s.append(chr(int.from_bytes(b[i:i+2],'big')))
        return ''.join(s)

# for xmb_file in root.glob('ts*.xmb'):
for tsk_file in root.glob(f'*.tsk'):
    print('-'*20)
    print(tsk_file)
    counter = Counter()
    tsk = open(tsk_file,'rb').read()
    xmb_ind = tsk.index(b'XMB ')
    data = o_data = tsk[xmb_ind:]
    # data = o_data = open(xmb_file,'rb').read()
    xmb_,data = read_slice(data,4)

    entry_count,data = read_slice(data,4,'int')
    attribute_count,data = read_slice(data,4,'int')
    string_count,data = read_slice(data,4,'int')
    mapped_entry_count,data = read_slice(data,4,'int')

    string_base_offset,data = read_slice(data,4,'int')
    entry_offset,data = read_slice(data,4,'int')
    attribute_offset,data = read_slice(data,4,'int')
    mapped_entry_offset,data = read_slice(data,4,'int')
    name_offset,data = read_slice(data,4,'int')
    value_offset,data = read_slice(data,4,'int')

    pad,data = read_slice(data,4*5)
    strings_offset_bytes,data = read_slice(data,4*string_count)
    string_offsets,tmp_b = [],strings_offset_bytes
    for i in range(string_count):
        string_offset,tmp_b = read_slice(tmp_b,4,'int')
        string_offsets.append(string_offset)
    
    print(f"""
entry_count:{entry_count}
attribute_count:{attribute_count}
string_count:{string_count}
mapped_entry_count:{mapped_entry_count}
""")
    
    print(f"""
string_base_offset:{string_base_offset}
entry_offset:{entry_offset}
attribute_offset:{attribute_offset}
mapped_entry_offset:{mapped_entry_offset}
name_offset:{name_offset}
value_offset:{value_offset}
string_offsets:{string_offsets}
""")
    

    entries_bytes = o_data[entry_offset:entry_offset + entry_count * Entry.size]
    entries = parse_entries(entries_bytes)
    print(f"found {entry_count}({len(entries)}) entries: ",entries)

    attributes_bytes = o_data[attribute_offset:attribute_offset + attribute_count * Attribute.size]
    attributes = parse_attributes(attributes_bytes)
    print(f"found {attribute_count}({len(attributes)}) attributes: ",attributes)

    mapped_entry_bytes = o_data[mapped_entry_offset:mapped_entry_offset + mapped_entry_count * Attribute.size]
    mapped_entries = parse_mapped_entries(mapped_entry_bytes)
    print(f"found {mapped_entry_count}({len(mapped_entries)}) attributes: ",mapped_entries)

    pair_bytes = o_data

    name_bytes = o_data[name_offset:]
    value_bytes = o_data[value_offset:]

    for attribute in attributes:
        attribute:Attribute
        name_off,value_off = attribute.name_offset,attribute.value_offset
        name,value = cut_value(name_bytes,name_off),cut_value(value_bytes,value_off)
        if not value:
            cut_value(value_bytes,value_off)
        attribute.name = name
        attribute.value = value
    
    attribute_map = {a.index:a for a in attributes}
    
    for entry in entries:
        entry:Entry
        entry.name = cut_value(name_bytes,entry.name_offset)
        att_count = entry.attribute_count
        att_start_index = entry.attribute_start_index
        for attrib_index in range(att_start_index,att_start_index+att_count):
            try:
                entry.attributes.append(attribute_map[attrib_index])
            except:
                print(entry,entry.attributes,attrib_index)
    
    root = None
    node_map = {}
    entries = sorted(entries,key = lambda z:z.parent_index)
    for e in entries:
        e:Entry
        if e.parent_index == -1:
            root = node = ElementTree.Element(e.name)
        else:
            parent = node_map[e.parent_index]
            node = ElementTree.SubElement(parent,e.name)
        for attrib in e.attributes:
            attrib:Attribute
            node.attrib[attrib.name] = attrib.value
        node_map[e.index] = node
    tree = ElementTree.ElementTree(root)
    tree.write(tsk_file.parent/(tsk_file.name+'_new.xml'))
    
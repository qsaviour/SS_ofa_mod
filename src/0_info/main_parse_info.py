a = '67 1D 65 E5 79 6D 00 00'
b = '00 59 00 6F 00 73 00 68 00 69 00 00'
c="00 43 00 48 00 41 00 4E 00 47 00 49 00 4E 00 27 00 20 00 4D 00 59 00 20 00 57 00 4F 00 52 00 4C 00 44 00 21 00 21 00 0A 59 09 30 8F 30 8B 4E 16 75 4C 30 67 66 1F 30 6E 30 88 30 46 30 6B 8F 1D 30 51 FF 01 00 0A 30 4D 30 89 30 81 30 4F 00 53 00 54 00 41 00 47 00 45 30 01 30 69 30 53 30 7E 30 67 30 82 90 32 30 82 30 46 FF 01 00 0A 59 09 30 8F 30 8A 59 CB 30 81 30 5F 4E 16 75 4C 30 78 30 6E 30 01 65 B0 30 5F 30 6A 30 8B 65 C5 7A CB 30 61 30 6E 60 F3 30 44 30 92 00 0A 8F BC 30 81 30 5F 30 D5 30 EC 30 C3 30 B7 30 E5 30 CA 30 F3 30 D0 30 FC 30 02 00 00 00 00 00 00"
def parse_s(s):
    s = s.split(' ')
    s = [''.join(s[i:i+2]) for i in range(0,len(s),2)]
    res = []
    for e in s:
        e = int(e,16)
        e = chr(e)
        res.append(e)
    return ''.join(res)

print(parse_s(a))
print(parse_s(b))
print(parse_s(c))
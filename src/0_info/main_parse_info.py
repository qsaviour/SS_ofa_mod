a = '52 00 49 00 4F 00 4E 00 41'
b = '51 85 75 30 54 F2 4E 5F'

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
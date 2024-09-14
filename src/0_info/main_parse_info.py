a = '30 4A 30 4A 30 4F 30 7C 30 72 30 8D 30 57'
b = '30 4A 30 4A 30 4F 30 7C 30 72 30 8D 30 57'

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
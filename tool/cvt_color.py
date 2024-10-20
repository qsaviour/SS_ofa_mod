
def cvt_color(v):
    if type(v) == str:
        v = int(v)
    if v == 0:
        h = '0'*6
    else:
        h = hex(v)[2:]
    a,b,c = h[:2],h[2:4],h[4:6]
    a,b,c = c,b,a
    a,b,c = map(lambda z:int(z,16),(a,b,c))
    print(a,b,c)
    a,b,c = a/255,b/255,c/255
    print(f"{a:0.2f},{b:0.2f},{c:0.2f}")

16777215
4227327
16711808
16744448
16711935
4259584
8454143
for v in ["8454143",]:
    cvt_color(v)


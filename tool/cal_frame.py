# bpm = 159 # col
# bpm = 170 #cng
# bpm = 163 # bnd
# bpm = 145 # meg
# bpm =  171 # jrA
bpm = 168 # ti2

while True:
    a = input()
    a = float(a)

    a = a / bpm * 60
    aa = int(a)//60
    b = (a - aa*60)
    b1,b2 = int(b) ,(b - int(b))*30/60
    b = b1+b2
    print(aa,":",f"{b:.2f}")

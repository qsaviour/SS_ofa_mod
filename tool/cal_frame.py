# bpm = 159 # col
bpm = 170 #cng
# bpm = 163 # bnd
# bpm = 145 # meg

while True:
    a = input()
    a = float(a)

    a = a / bpm * 60
    aa = int(a)//60
    b = (a - aa)
    b1,b2 = int(b) ,(b - int(b))*30/100
    b = b1+b2
    print(aa,":",f"{b:.2f}")

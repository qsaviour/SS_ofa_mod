# bpm = 159 # col
bpm = 170 #cng
while True:
    a = input()
    a,b = a.split('.')
    a,b = map(int,(a,b))
    frames = a+b/30
    beats = frames/60*bpm
    print(beats)
import random

fout = open('pharmacies_in.txt', 'w')
ctr = 1
additional = 178
with open('places_india.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        elems = line.split(':')
        lat = float(elems[1])
        long = float(elems[2])
        for i in range(0, additional):
            new_lat = lat + random.uniform(-0.1, 0.1)
            new_long = long + random.uniform(-0.1, 0.1)
            fout.write(str(ctr)+":"+str(new_lat)+":"+str(new_long)+":"+elems[3])
            ctr += 1
fout.close()

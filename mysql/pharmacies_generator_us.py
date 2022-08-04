import random

fout = open('pharmacies_us.txt', 'w')
ctr = 1
additional = 8
with open('us_places.csv', 'r') as f:
    lines = f.readlines()
    for line in lines:
        elems = line.split(',')
        lat = float(elems[-2])
        long = float(elems[-1])
        for i in range(0, additional):
            new_lat = lat + random.uniform(-0.1, 0.1)
            new_long = long + random.uniform(-0.1, 0.1)
            fout.write(str(ctr)+":"+str(new_lat)+":"+str(new_long)+":"+elems[0]+" "+elems[1]+'\n')
            ctr += 1
fout.close()

from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
import random


cls = Cluster()
session = cls.connect('drug_repo')
pharmacy_lat_long_list = []
NO_OF_DRUGS = 7675
rand_array = [0, 0, 0, 0, 0, 1]
QUANTITY_LIMIT = 30

with open('pharmacies_US.txt', 'r') as f:
    lines = f.readlines()
    ctr = 0
    for line in lines:
        elems = line.split(":")
        pharm_id = int(elems[0])
        lat = float(elems[1])
        long = float(elems[2])
        pharmacy_lat_long_list.append([lat, long])

batch = BatchStatement()
ctr = 0
for i in range (4150, NO_OF_DRUGS + 1):
    for j in range (0, len(pharmacy_lat_long_list)):
        rand_no = rand_array[random.randint(0, len(rand_array) - 1)]
        if rand_no == 1:
            # add this pharmacy (j + 1) to the drug
            lat_long = pharmacy_lat_long_list[j]
            sql = "INSERT INTO drug_pharma (drug_id, pharma_id, lat_long, quantity) VALUES (%s, %s, %s, %s)"
            values_tuple = (i, j + 1, lat_long, random.randint(1, QUANTITY_LIMIT))
            batch.add(sql, values_tuple)
            ctr += 1
            if ctr % 100 == 0:
                session.execute(batch)
                #print("Executed "+str(ctr)+" stmts")
                batch = BatchStatement()
    print("Done for drug "+str(i))

session.execute(batch)
print("Executed remaining")

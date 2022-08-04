from cassandra.cluster import Cluster
import random
from time import time
import math
import functools

def distance_calc(pharmacy):
    return math.sqrt(math.pow(curr_lat - pharmacy.lat, 2) + math.pow(curr_long - pharmacy.long, 2))

class Pharmacy:
    def __init__(self, pharm_id, lat, long, quantity):
        self.pharm_id = pharm_id
        self.lat = lat
        self.long = long
        self.quantity = quantity
    def __str__(self):
        return "("+str(self.pharm_id)+", "+str(self.lat)+", "+str(self.long)+", "+str(distance_calc(self))+", "+str(self.quantity)+")"

def my_comparator(pharmacy_1, pharmacy_2):
    distance_1 = distance_calc(pharmacy_1)
    distance_2 = distance_calc(pharmacy_2)
    if(distance_1 < distance_2):
        return -1
    else:
        return 1

cls = Cluster()
session = cls.connect('drug_repo')

NO_OF_TIMES = 5
total_time = 0.0
NO_OF_DRUGS = 7675
PHARM_LIMIT = 5
arb_lat_long = [
    (40.4256, -79.9311),
    (42.3955, -99.5361),
    (31.5896, -95.5671),
    (34.8688, -109.4238),
    (28.5213, -81.3871)

]
curr_lat = 0.0
curr_long = 0.0
SQL = "SELECT pharma_id, lat_long, quantity FROM drug_pharma WHERE drug_id = ?"
CQL_PHARMA = "SELECT name, address FROM pharmacy WHERE pharma_id IN "
for i in range(0, NO_OF_TIMES):
    drug_id = random.randint(1, NO_OF_DRUGS)
    stmt = session.prepare(SQL)
    query = stmt.bind([drug_id])
    startTime = time()
    res = session.execute(query)
    pharmacy_list = []
    for row in res:
        pharma_id = int(row[0])
        lat = float(row[1][0])
        long = float(row[1][1])
        quantity = int(row[2])
        p = Pharmacy(pharma_id, lat, long, quantity)
        pharmacy_list.append(p)
    curr_lat = arb_lat_long[i][0]
    curr_long = arb_lat_long[i][1]
    pharmacy_list = sorted(pharmacy_list, key = functools.cmp_to_key(my_comparator))[0: PHARM_LIMIT]
    pharm_args = "("
    for j in range (0, PHARM_LIMIT - 1):
        #print(pharmacy_list[j])
        pharm_args += (str(pharmacy_list[j].pharm_id) + ",")
    pharm_args += (str(pharmacy_list[PHARM_LIMIT - 1].pharm_id) + ")")
    cql_full = CQL_PHARMA + pharm_args
    print(pharm_args)
    pharm_details = session.execute(cql_full)
    endTime = time()
    timeTaken = endTime - startTime
    total_time += timeTaken
    j = 0
    for pharm_row in pharm_details:
        print(str(pharm_row)+", "+str(pharmacy_list[j]))

print("avg time "+str(total_time/NO_OF_TIMES))

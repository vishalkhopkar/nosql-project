import redis
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

r = redis.Redis()
NO_OF_DRUGS = 7675
NO_OF_TIMES = 5
LIMIT = 5

arb_lat_long = [
    (40.4256, -79.9311),
    (42.3955, -99.5361),
    (31.5896, -95.5671),
    (34.8688, -109.4238),
    (28.5213, -81.3871)

]
curr_lat = 0.0
curr_long = 0.0
total_time = 0.0

def my_comparator(pharmacy_1, pharmacy_2):
    distance_1 = distance_calc(pharmacy_1)
    distance_2 = distance_calc(pharmacy_2)
    if(distance_1 < distance_2):
        return -1
    else:
        return 1

for i in range (0, NO_OF_TIMES):
    drug_id = random.randint(1, NO_OF_DRUGS)
    key = "drug:"+str(drug_id)
    print("Searching for "+key)
    startTime = time()
    pharmacies_dict = r.hgetall(key)
    pharmacies = []
    lat_long_search = []
    for k in pharmacies_dict:
        lat_long_search.append(int(k))
    lats = r.hmget("lat", lat_long_search)
    longs = r.hmget("long", lat_long_search)
    ctr = 0
    for k in pharmacies_dict:
        pharm_id = int(k)
        quantity = int(pharmacies_dict[k])
        pharm_lat = float(lats[ctr])
        pharm_long = float(longs[ctr])
        ctr += 1
        p = Pharmacy(pharm_id, pharm_lat, pharm_long, quantity)
        #print("Added pharmacy "+str(pharm_id)+" to list")
        pharmacies.append(p)
    curr_lat = arb_lat_long[i][0]
    curr_long = arb_lat_long[i][1]
    sorted_list = sorted(pharmacies, key=functools.cmp_to_key(my_comparator))
    sorted_list = sorted_list[0:LIMIT]
    for j in range (0, LIMIT):
        print(sorted_list[j])
        pharm_key = "pharm:"+str(sorted_list[j].pharm_id)
        pharm_details = r.hgetall(pharm_key)
        for k1 in pharm_details:
            print(str(k1)+" : "+str(pharm_details[k1]))
    endTime = time()
    timeTaken = endTime - startTime
    total_time += timeTaken
    print("Time taken "+str(timeTaken)+"\n")

print("Avg time "+str(total_time/NO_OF_TIMES))

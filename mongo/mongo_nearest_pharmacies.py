from pymongo import MongoClient
import random
import functools
from time import time
import math

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

client = MongoClient("localhost")
db = client.drug_repo

NO_OF_TIMES = 5
NO_OF_DRUGS = 7675
PHARM_LIMIT = 5
total_time = 0.0
arb_lat_long = [
    (40.4256, -79.9311),
    (42.3955, -99.5361),
    (31.5896, -95.5671),
    (34.8688, -109.4238),
    (28.5213, -81.3871)

]
curr_lat = 0.0
curr_long = 0.0

for i in range (0, NO_OF_TIMES):
    drug_id = random.randint(1, NO_OF_DRUGS)
    print("SEARCHING FOR DRUG "+str(drug_id))
    startTime = time()
    pharmacies = db.drugs.find_one({'_id': drug_id}, {'_id': 0, 'pharmacies': 1})
    pharmacy_map = pharmacies['pharmacies']
    pharmacy_list = []
    for pharmacy in pharmacy_map:
        p = Pharmacy(pharmacy['_id'], pharmacy['lat'], pharmacy['long'], pharmacy['quantity'])
        pharmacy_list.append(p)
    curr_lat = arb_lat_long[i][0]
    curr_long = arb_lat_long[i][1]
    pharmacy_list_sorted = sorted(pharmacy_list, key=functools.cmp_to_key(my_comparator))[0: PHARM_LIMIT]
    for pharmacy in pharmacy_list_sorted:
        pharm_detail_dict = db.pharmacies.find_one({'_id': pharmacy.pharm_id})
        name = pharm_detail_dict['name']
        address = pharm_detail_dict['address']
        print(str(pharmacy)+" "+name+" "+address)
    endTime = time()
    timeTaken = endTime - startTime
    total_time += timeTaken

print("AVG TIME "+str(total_time/NO_OF_TIMES))

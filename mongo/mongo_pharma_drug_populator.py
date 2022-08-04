from pymongo import MongoClient
import random

class Pharmacy:
    def __init__(self, pharm_id, lat, long, name, address):
        self.pharm_id = pharm_id
        self.lat = lat
        self.long = long
        self.name = name
        self.address = address
    def __str__(self):
        return "("+str(self.pharm_id)+", "+str(self.lat)+", "+str(self.long)+", "+str(distance_calc(self))+")"

client = MongoClient("localhost")
db = client.drug_repo

drug_list = []
pharmacy_list = []
rand_us_names = ["CVS Pharm", "Walgreens", "Giant Eagle", "Rite Aid", "Walmart", "Kroger", "Albertsons", "Publix", "Costco", "Pharmareica"
                "Cardinal Health", "McKeeson", "Hy Vee", "AmerisourceBergen", "Ahold Delhaize", "H E B Grocery", "Meijer Great Lakes",
                "Southeastern Grocers", "Kaiser Permanente", "Wegmans Food Markets", "Kinney Drugs"]
rand_us_names_len = len(rand_us_names)
rand_array = [0, 0, 0, 0, 0, 1]
QUANTITY_LIMIT = 30

with open ('fda_drugs.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        elems = line.split(',')
        drug_name = ""
        elems_len = len(elems)
        for i in range(1, elems_len):
            drug_name += elems[i]
        drug_name = drug_name.strip()
        drug_list.append(drug_name)

with open ('pharmacies_US.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        elems = line.split(":")
        # pharm_id:lat:long:address
        pharm_id = int(elems[0])
        lat = float(elems[1])
        long = float(elems[2])
        address = elems[3]
        name = rand_us_names[random.randint(0, rand_us_names_len - 1)]
        p = Pharmacy(pharm_id, lat, long, name, address)
        pharmacy_list.append(p)

# Inserting pharmacies
'''
json_list = []
for i in range(0, len(pharmacy_list)):
    json = {
        '_id' : i + 1,
        'name' : pharmacy_list[i].name,
        'address' : pharmacy_list[i].address
    }
    json_list.append(json)
db.pharmacies.insert_many(json_list)
print("All pharmacies inserted")
# Inserting drugs
'''
json_list = []
for i in range(4746, len(drug_list)):
    pharmacies = []
    for j in range (0, len(pharmacy_list)):
        rand_no = rand_array[random.randint(0, len(rand_array) - 1)]
        if rand_no == 1:
            pharm_json = {
                '_id': pharmacy_list[j].pharm_id,
                'quantity': random.randint(1, QUANTITY_LIMIT),
                'lat': pharmacy_list[j].lat,
                'long': pharmacy_list[j].long
            }
            pharmacies.append(pharm_json)

    json = {
        '_id' : i + 1,
        'name' : drug_list[i],
        'pharmacies': pharmacies
    }
    json_list.append(json)
    db.drugs.insert_one(json)
    print("Drug "+str(i + 1)+" inserted")

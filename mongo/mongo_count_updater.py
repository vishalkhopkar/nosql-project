from pymongo import MongoClient
from time import time

client = MongoClient("localhost")
db = client.drug_repo

DRUG_ID = 1782
PHARM_IDS = [60932, 59623, 57333, 25629, 8433]
total_time = 0.0
for i in range (0, len(PHARM_IDS)):
    startTime = time()
    res = db.drugs.update_one({'_id':DRUG_ID, 'pharmacies._id': PHARM_IDS[i]}, {'$inc' : {'pharmacies.$.quantity': -1}})
    endTime = time()
    timeTaken = endTime - startTime
    total_time += timeTaken
    if res.modified_count == 1:
        print("Successful for "+str(PHARM_IDS[i]))

print("avg time "+str(total_time/len(PHARM_IDS)))

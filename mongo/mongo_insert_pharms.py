from pymongo import MongoClient
from time import time

client = MongoClient("localhost")
db = client.drug_repo

DRUG_ID = 1782
PHARM_IDS = [60932, 59623, 57333, 25629, 8433]
lat_long = [
    (40.45476789983778, -76.35676196657934),
    (41.56372081194251, -80.21270987209849),
    (41.67477131740529, -69.9625053591134),
    (44.59025798539508, -90.16238319871293),
    (39.167051582813066, -84.64342368432315)

]
total_time = 0.0
for i in range (0, len(PHARM_IDS)):
    push_dict = {
      '$push':
        {
            'pharmacies':
            {
                '$each': [{ '_id' : PHARM_IDS[i], 'lat' : lat_long[i][0], 'long': lat_long[i][1]}]
            }
        }
    }
    startTime = time()
    res = res = db.drugs.update_one({'_id': DRUG_ID}, push_dict)
    endTime = time()
    timeTaken = endTime - startTime
    total_time += timeTaken
    if res.modified_count == 1:
        print("Successful for "+str(PHARM_IDS[i]))

print("avg time "+str(total_time/len(PHARM_IDS)))

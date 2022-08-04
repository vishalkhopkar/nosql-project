import redis
import random

r = redis.Redis()
latDict = {}
longDict = {}
rand_us_names = ["CVS Pharm", "Walgreens", "Giant Eagle", "Rite Aid", "Walmart", "Kroger", "Albertsons", "Publix", "Costco", "Pharmareica"
                "Cardinal Health", "McKeeson", "Hy Vee", "AmerisourceBergen", "Ahold Delhaize", "H E B Grocery", "Meijer Great Lakes",
                "Southeastern Grocers", "Kaiser Permanente", "Wegmans Food Markets", "Kinney Drugs"]
rand_us_names_len = len(rand_us_names)

with open ('pharmacies_US.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        elems = line.split(":")
        # pharm_id:lat:long:address
        pharm_id = int(elems[0])
        lat = float(elems[1])
        long = float(elems[2])
        address = elems[3]
        latDict[pharm_id] = lat
        longDict[pharm_id] = long
        pharm_dict = {}
        pharm_dict['name'] = rand_us_names[random.randint(0, rand_us_names_len - 1)]
        pharm_dict['address'] = address
        r.hmset("pharm:"+elems[0], pharm_dict)
        print("Set lat long for "+elems[0])
    r.hmset("lat", latDict)
    r.hmset("long", longDict)
    print("Lat and long set")

import redis
import random

r = redis.Redis()
rand_array = [0, 0, 0, 0, 0, 1]
rand_array_size = len(rand_array)
NO_OF_DRUGS = 7675
NO_OF_PHARMACIES = 62592
QUANTITY_LIMIT = 30

for i in range (1, NO_OF_DRUGS + 1):
    dict = {}
    for j in range (1, NO_OF_PHARMACIES + 1):
        should_pharmacy_be_added = rand_array[random.randint(0, rand_array_size - 1)]
        if should_pharmacy_be_added == 1:
            dict[j] = random.randint(1, QUANTITY_LIMIT)
    drug_key = "drug:"+str(i)
    r.hmset(drug_key, dict)
    print("Set for "+drug_key)

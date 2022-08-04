import redis
from time import time

r = redis.Redis()
drug_key = "drug:10"
pharmacies = [54332, 51056, 61316, 61987, 61462]
NO_OF_TIMES = 5
total_time = 0.0
for i in range(0, NO_OF_TIMES):
    startTime = time()
    r.hincrby(drug_key, pharmacies[i], 1)
    endTime = time()
    timeTaken = endTime - startTime
    total_time += timeTaken
print("Avg time "+str(total_time/NO_OF_TIMES))

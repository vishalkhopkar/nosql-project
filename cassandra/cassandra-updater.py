from cassandra.cluster import Cluster
from time import time

cls = Cluster()
session = cls.connect('drug_repo')

drug_id = 842
pharm_ids = [1803, 2422, 3007, 6041, 62569]
PHARM_IDS_LEN = len(pharm_ids)
UPDATE_TO = 2
CQL = "UPDATE drug_pharma SET quantity = 2 WHERE drug_id = 842 AND pharma_id = ?"
total_time = 0.0
for i in range(0, PHARM_IDS_LEN):
    stmt = session.prepare(CQL)
    query = stmt.bind([pharm_ids[i]])
    startTime = time()
    session.execute(query)
    endTime = time()
    timeTaken = endTime - startTime
    total_time += timeTaken

print("AVG TIME "+str(total_time/PHARM_IDS_LEN))

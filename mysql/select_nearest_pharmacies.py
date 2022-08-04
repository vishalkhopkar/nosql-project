import mysql.connector
import random
from time import time

mydb = mysql.connector.connect(
  host="localhost",
  user="vishal",
  password="thegambia",
  database="drug_repo1"
)
NO_OF_DRUGS = 7675
NO_OF_TIMES = 5
lat_long = [
    (40.4256, -79.9311),
    (42.3955, -99.5361),
    (31.5896, -95.5671),
    (34.8688, -109.4238),
    (28.5213, -81.3871)

]
print(mydb)
mycursor = mydb.cursor()
total_time = 0
sql = """SELECT A.name, A.address, A.latitude, A.longitude, SQRT(POWER(%s - A.latitude, 2) + POWER(%s - A.longitude, 2))
 AS distance FROM pharmacy A INNER JOIN pharma_drug B ON A.id = B.pharma_id WHERE drug_id = %s ORDER BY distance LIMIT 5"""
# run this randomly for different drug ids and lat long
for i in range (0, NO_OF_TIMES):
    drug_id = random.randint(1, NO_OF_DRUGS)
    values = (lat_long[i][0], lat_long[i][1], drug_id)
    startTime = time()
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    endTime = time()
    time_taken = endTime - startTime
    total_time += time_taken
    print("Took "+str(time_taken)+" seconds")
    for x in myresult:
        print(x)

print("Avg time "+str(total_time/NO_OF_TIMES))

import mysql.connector
import random

mydb = mysql.connector.connect(
  host="localhost",
  user="vishal",
  password="thegambia",
  database="drug_repo1"
)

print(mydb)
mycursor = mydb.cursor()
sql = "INSERT INTO drug VALUES (%s, %s)"
commit_length = 100
ctr = 0
vals = []
with open ('fda_drugs.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        elems = line.split(",")
        # elems[0] is the id, rest is the drug name
        drug_name = ''
        for i in range (1, len(elems)):
            drug_name += elems[i]
        drug_name = drug_name.strip()
        drug_id = int(elems[0])
        val_tuple = (drug_id, drug_name)
        vals.append(val_tuple)
        ctr += 1
        if ctr == commit_length:
            mycursor.executemany(sql, vals)
            mydb.commit()
            print(mycursor.rowcount, "were inserted.")
            ctr = 0
            vals = []
# commit any remaining data left
if len(vals) > 1:
    mycursor.executemany(sql, vals)
    mydb.commit()

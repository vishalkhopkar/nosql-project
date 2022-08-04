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

country = input('Choose country 1: US 2: IN\n')
drugs_file_name = ''
pharma_file_name = ''
country_code = ''
if country == '1':
    drugs_file_name = 'fda_drugs.txt'
    pharma_file_name = 'pharmacies_US.txt'
    country_code = 'US'
else:
    drugs_file_name = 'cdsco_drugs.txt'
    pharma_file_name = 'pharmacies_in.txt'
    country_code = 'IN'

pharmacies_count = 0
drugs_count = 0

# 15% chance that a drug is available
avbl_list = [0, 0, 0, 0, 0, 1]
len_avbl_list = len(avbl_list)
with open(drugs_file_name, 'r') as fp:
    drugs_count = 7675
with open(pharma_file_name, 'r') as fp:
    pharmacies_count = len(fp.readlines())

ctr = 0
commit_count = 1000
vals = []
sql = "INSERT INTO pharma_drug VALUES (%s, %s, %s)"
for i in range (17686, pharmacies_count):
    print("Data for pharmacy "+str(i + 1))
    for j in range (0, drugs_count):
        rand_index = random.randint(0, len_avbl_list - 1)
        if avbl_list[rand_index] == 1:
            # drug (j + 1) is available at pharmacy (i + 1)
            quantity = random.randint(1, 30)
            val_tuple = (i + 1, j + 1, quantity)
            vals.append(val_tuple)
            ctr += 1
            if ctr == commit_count:
                mycursor.executemany(sql, vals)
                mydb.commit()
                print(mycursor.rowcount, "were inserted.")
                ctr = 0
                vals = []

# commit any remaining data left
if len(vals) > 1:
    mycursor.executemany(sql, vals)
    mydb.commit()

print(mycursor.rowcount, "were inserted.")

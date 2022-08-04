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
rand_us_names = ["CVS Pharm", "Walgreens", "Giant Eagle", "Rite Aid", "Walmart", "Kroger", "Albertsons", "Publix", "Costco", "Pharmareica"
                "Cardinal Health", "McKeeson", "Hy Vee", "AmerisourceBergen", "Ahold Delhaize", "H E B Grocery", "Meijer Great Lakes",
                "Southeastern Grocers", "Kaiser Permanente", "Wegmans Food Markets", "Kinney Drugs"]
vals = []
no_of_pharm_names = len(rand_us_names)
commit_length = 100
ctr = 0
sql = "INSERT INTO pharmacy VALUES (%s, %s, %s, %s, %s)"
with open ('pharmacies_US.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        elems = line.split(':')
        pharmId = int(elems[0])
        name = rand_us_names[random.randint(0, no_of_pharm_names - 1)]
        latitude = float(elems[1])
        longitude = float(elems[2])
        address = elems[3]
        val_tuple = (pharmId, name, latitude, longitude, address)
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

print(mycursor.rowcount, "were inserted.")


mydb.commit()

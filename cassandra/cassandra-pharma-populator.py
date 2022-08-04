from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
import random


cls = Cluster()
session = cls.connect('drug_repo')
pharmacy_lat_long_list = []
NO_OF_DRUGS = 7675
rand_us_names = ["CVS Pharm", "Walgreens", "Giant Eagle", "Rite Aid", "Walmart", "Kroger", "Albertsons", "Publix", "Costco", "Pharmareica",
                "Cardinal Health", "McKeeson", "Hy Vee", "AmerisourceBergen", "Ahold Delhaize", "H E B Grocery", "Meijer Great Lakes",
                "Southeastern Grocers", "Kaiser Permanente", "Wegmans Food Markets", "Kinney Drugs"]
rand_us_names_len = len(rand_us_names)
rand_array = [0, 0, 0, 0, 0, 1]
QUANTITY_LIMIT = 30

with open('pharmacies_US.txt', 'r') as f:
    lines = f.readlines()
    batch = BatchStatement()
    ctr = 0
    for line in lines:
        elems = line.split(":")
        pharm_id = int(elems[0])
        lat = float(elems[1])
        long = float(elems[2])
        pharmacy_lat_long_list.append((lat, long))
        address = elems[3]
        name = rand_us_names[random.randint(0, rand_us_names_len - 1)]
        batch.add(SimpleStatement("INSERT INTO pharmacy (pharma_id, name, address) VALUES (%s, %s, %s)"), (pharm_id, name, address))
        ctr += 1
        if ctr % 100 == 0:
            session.execute(batch)
            print("Executed "+str(ctr)+" statements")
            batch = BatchStatement()

    session.execute(batch)

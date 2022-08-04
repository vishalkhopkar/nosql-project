from neo4j import GraphDatabase
import random

def create_pharmacy(tx, query):
    tx.run(query)

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "thegambia"))
rand_us_names = ["CVS Pharm", "Walgreens", "Giant Eagle", "Rite Aid", "Walmart", "Kroger", "Albertsons", "Publix", "Costco", "Pharmareica",
                "Cardinal Health", "McKeeson", "Hy Vee", "AmerisourceBergen", "Ahold Delhaize", "H E B Grocery", "Meijer Great Lakes",
                "Southeastern Grocers", "Kaiser Permanente", "Wegmans Food Markets", "Kinney Drugs"]
rand_us_names_len = len(rand_us_names)
queries = ""
with driver.session() as session:
    with open ('pharmacies_US.txt', 'r') as f:
        lines = f.readlines()
        ctr = 0
        for line in lines:
            elems = line.split(':')
            pharma_id = elems[0]
            lat = elems[1]
            long = elems[2]
            address = elems[3]
            address = address.replace('\n','')
            address = address.replace("'", "")
            name = rand_us_names[random.randint(0, rand_us_names_len - 1)]

            cypher = "CREATE (p"+pharma_id+":Pharmacy {id:"+pharma_id+", name:'"+name+"', address:'"+address+"', lat:"+lat+", long:"+long+"})"
            queries += (cypher + '\n')
            ctr += 1
            if ctr % 8000 == 0:
                session.write_transaction(create_pharmacy, queries)
                queries = ""
                print("Inserted "+str(ctr)+" records")

    session.write_transaction(create_pharmacy, queries)
    print("Inserted rem records")
driver.close()

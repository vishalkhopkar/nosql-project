from neo4j import GraphDatabase
import random

def create_pharmacy(tx, query):
    tx.run(query)

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "thegambia"))
NO_OF_DRUGS = 7675
NO_OF_PHARMACIES = 62592
RAND_BOUND = 6
QUANTITY_LIMIT = 30
queries = ""
ctr = 0
with driver.session() as session:
    for i in range(0, NO_OF_DRUGS):
        for j in range (0, NO_OF_PHARMACIES):
            # (i + 1) -> drug id, (j + 1) -> pharma id
            rand_no = random.randint(1, RAND_BOUND)
            if rand_no == 1:
                quantity = random.randint(1, QUANTITY_LIMIT)
                ctr += 1
                cypher = "MATCH (d"+str(i + 1)+":Drug), (p"+str(j + 1)+":Pharmacy) USING INDEX d"+str(i + 1)+":Drug(id) USING INDEX p"+str(j + 1)+":Pharmacy(id) WHERE d"+str(i + 1)+".id = "+str(i + 1)+" AND p"+str(j + 1)+".id = "+str(j + 1)+" CREATE (d"+str(i + 1)+")-[:AVAILABLE_AT {quantity:"+str(quantity)+"}]->(p"+str(j + 1)+")"
                if ctr % 1000 != 0:
                    cypher += ("WITH p"+str(j + 1)+" as p"+str(j + 1))
                queries += (cypher + "\n")

                if ctr % 1000 == 0:
                    session.write_transaction(create_pharmacy, queries)
                    queries = ""
                    print("Inserted "+str(ctr)+" records")




driver.close()
'''
MATCH (d7675:Drug), (p1:Pharmacy) WHERE d7675.id = 7675 AND p1.id = 1 CREATE (d7675)-[:AVAILABLE_AT]->(p1)
WITH d7675 as d767
MATCH (d7674:Drug), (p3:Pharmacy) WHERE d7674.id = 7674 AND p3.id = 3 CREATE (d7674)-[:AVAILABLE_AT]->(p3)
'''

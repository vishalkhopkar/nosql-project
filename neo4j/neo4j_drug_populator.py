from neo4j import GraphDatabase

def create_drug(tx, query):
    tx.run(query)

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "thegambia"))
NO_OF_DRUGS = 7675
drug_list = []
queries = ""
with open ('fda_drugs.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        elems = line.split(',')
        drug_name = ""
        elems_len = len(elems)
        for i in range(1, elems_len):
            drug_name += elems[i]
        drug_name = drug_name.strip()
        drug_name = drug_name.replace("'", "")
        drug_list.append(drug_name)


with driver.session() as session:
    for i in range(0, len(drug_list)):
        cypher = "CREATE (drug"+str(i + 1)+":Drug {id:"+str(i + 1)+", name:'"+drug_list[i]+"'})"
        queries += (cypher + '\n')
    session.write_transaction(create_drug, queries)
driver.close()

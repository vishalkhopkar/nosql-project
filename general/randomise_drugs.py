import random

# there is a 33% chance that the drug is not available at the pharmacy
# if it is, random quantities between 1-30
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

# 33% chance not avbl, 66% chance of being available
avbl_list = [0, 1, 1]

with open(drugs_file_name, 'r') as fp:
    drugs_count = 3723
with open(pharma_file_name, 'r') as fp:
    pharmacies_count = len(fp.readlines())

fout = open('pharma_drugs_'+country_code+'.txt', 'w')
for i in range (0, pharmacies_count):
    print("Data for pharmacy "+str(i + 1))
    for j in range (0, drugs_count):
        rand_index = random.randint(0, 2)
        if avbl_list[rand_index] == 1:
            # drug (j + 1) is available at pharmacy (i + 1)
            quantity = random.randint(1, 30)
            fout.write(str(i + 1)+","+str(j + 1)+","+str(quantity)+"\n")
fout.close()

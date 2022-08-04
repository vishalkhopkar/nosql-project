
country = input('Find max drug length in 1: US 2: IN\n')
file_name = ''
if country == '1':
    file_name = 'fda_drugs.txt'
else:
    file_name = 'cdsco_drugs.txt'

max_length = 0

with open(file_name, 'r') as f:
    lines = f.readlines()
    for line in lines:
        elems = line.split(',')
        if len(elems) >= 2:
            drug_name = elems[1]
            drug_name_length = len(drug_name)
            if drug_name_length > max_length:
                max_length = drug_name_length

print(max_length)

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="vishal",
  password="thegambia",
  database="drug_repo1"
)

print(mydb)
mycursor = mydb.cursor()

sql_select = "SELECT distinct address FROM pharmacy"
sql_update = "UPDATE pharmacy SET address = %s, STATE = %s WHERE address = %s"
mycursor.execute(sql_select)
result = mycursor.fetchall()
vals = []
for x in result:
    address = x[0]
    orig_address = address
    address = address.strip()
    address_elems = address.split(" ")
    state = address_elems[-1]
    address = ""
    for i in range (0, len(address_elems) - 1):
        address += (address_elems[i]+" ")
    address = address.strip()
    val_tuple = (address, state, orig_address)
    print("Adding for update "+address, state)
    mycursor.execute(sql_update, val_tuple)
    mydb.commit()

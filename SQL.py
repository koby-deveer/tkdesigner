# Importing module
import mysql.connector

# Creating connection object

def SQL_IN(data):
	mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "valcoscale12345@",
	database="VALCO_RECORDS"
	)

	# Printing the connection object
	print(mydb)
	cursor=mydb.cursor()
	dbFunc="INSERT INTO WEIGHIN VALUES(NULL,%s,%s,%s,%s)"
	cursor.execute(dbFunc,data)
	mydb.commit()
	
	mydb.close()



def SQL_OUT(data):
	mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "valcoscale12345@",
	database="VALCO_RECORDS"
	)

	print(mydb)
	cursor=mydb.cursor()
	dbFunc="INSERT INTO WEIGHOUT VALUES(NULL,%s,%s,%s,%s,%s,%s)"
	cursor.execute(dbFunc,data)
	mydb.commit()
	mydb.close()

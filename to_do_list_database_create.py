import mysql.connector

conn=mysql.connector.connect(
	 host="localhost",
	 username="root",
	 password="Mysql@123")

cursor=conn.cursor()

query="""CREATE database if not exists to_do_list_db"""

cursor.execute(query)

print("all databases available:")

query="""SHOW databases"""

cursor.execute(query)

result=cursor.fetchall()

for row in result:

	print(row[0])

conn.commit()

cursor.close()

conn.close()
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


def db_connection():

	try:
		connection=mysql.connector.connect(
			host="localhost",
			user="root",
			password="Mysql@123",
			database="to_do_list_db")

		print("connected to mysql database name : to_do_list")

		cursor=connection.cursor()

		query="""CREATE TABLE if not exists to_dos (
			     task_id   int AUTO_INCREMENT  PRIMARY KEY,
			     task_name varchar(255),
			     status    VARCHAR(255),
			     category  SET("finance","accounting","health","gardening","studying"),
			     completing_date  datetime,
			     user_id   int
			      )"""

		cursor.execute(query)

		query="""CREATE TABLE if  not exists users(
        	     user_id    int  PRIMARY KEY ,
        	     user_name  varchar(255),
        	     address    varchar(255))"""

		cursor.execute(query)

		return connection


	except mysql.connector.Error as error:

		print("some error occured:",error)

		return jsonify(error="connection not established"),500

db_connection()

conn.commit()

cursor.close()

conn.close()
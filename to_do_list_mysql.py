import mysql.connector

from flask import Flask,request,jsonify

app=Flask(__name__)

def db_connection():

	try:

		connection=mysql.connector.connect(
			host="localhost",
			user="root",
			password="Mysql@123",
			database="to_do_list_db")

		print("connected to mysql database name : to_do_list")

		cursor=connection.cursor()

		query="""CREATE TABLE if not exists to_do_list_tabl (
			     task_id   int    PRIMARY KEY,
			     task_name varchar(255),
			     status    varchar(255) ,
			     category  varchar(255),
			     completing_date  datetime
			      )"""


		cursor.execute(query)

		return connection

	except mysql.connector.Error as error:

		print("some error occured:",error)

		return None
    

@app.route('/to_do_list',methods=["GET"])

def get_to_do_list():

	conn=db_connection()

	cur=conn.cursor()

	query="""SELECT * from to_do_list_tabl"""

	cur.execute(query)

	result=cur.fetchall()

	to_do_list=[
	           {"task_id":row[0],
	           "task_name":row[1],
			    "status":row[2],
			    "category":row[3],
			    "completing_date":row[4],
			 
			   }
			   for row in result]

	cur.close()

	conn.close()

	return (jsonify(to_do_list))

@app.route('/to_do_list',methods=["POST"])

def insert_task():

	conn=db_connection()

	cursor=conn.cursor()

	query=""" INSERT INTO to_do_list_tabl 
	          (task_id,task_name,status,category,completing_date)
	          VALUES(%s,%s,%s,%s,%s)"""

	task_id=request.form["task_id"]
	task_name=request.form["task_name"]
	status=request.form["status"]
	category=request.form["category"]
	completing_date=request.form["completing_date"]


	cursor.execute(query,(task_id,task_name,status,category,completing_date))

	conn.commit()

	cursor.close()

	conn.close()

	updated_list={"task_id":task_id,
	              "task_name":task_name,
	              "status":status,
	              "category":category,
	              "completing_date":completing_date,
	              }


	return jsonify(updated_list)

@app.route("/to_do_list/<int:id>",methods=["DELETE"])

def delete_task(id):

	conn=db_connection()

	cursor=conn.cursor()

	query="""SELECT task_id from to_do_list_tabl
	         where task_id=%s"""
    
	cursor.execute(query,(id,))

	result=cursor.fetchone()

	if result:

		query="""DELETE FROM to_do_list_table
		         where task_id=%s"""

		cursor.execute(query,(id,))

		conn.commit()

		cursor.close()

		conn.close()

		return "task with task_id {} deleted from to_do_list ".format(id)

	conn.commit()

	cursor.close()

	conn.close()

	return "task with task_id doesn't exist in your to_do_list"

@app.route("/to_do_list/<int:id>",methods=["PATCH"])

def update_task(id):

	conn=db_connection()

	cursor=conn.cursor()

	task_name=request.form["task_name"]

	query="""UPDATE to_do_list_tabl
	         SET task_name=%s
	         WHERE task_id=%s"""

	cursor.execute(query,(task_name,id))

	status=request.form["status"]

	query="""UPDATE to_do_list_tabl
	         SET status=%s
	         where task_id=%s"""

	cursor.execute(query,(status,id))

	completing_date=request.form["completing_date"]

	query="""UPDATE to_do_list_table
	         SET completing_date=%s
	         where task_id=%s"""

	cursor.execute(query,(completing_date,id))

	category=request.form["category"]

	query="""UPDATE to_do_list_tabl
	         SET category=%s
	         where task_id=%s"""

	cursor.execute(query,(category,id))

	conn.commit()

	cursor.close()

	conn.close()

	return "task updated"


if __name__=="__main__":

	app.run(debug=True)
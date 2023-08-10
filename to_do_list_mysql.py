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

		query="""CREATE TABLE if not exists to_do_list_table1 (
			     task_id   int AUTO_INCREMENT  PRIMARY KEY,
			     task_name varchar(255),
			     status    varchar(255),
			     category  varchar(255),
			     completing_date  datetime,
			     user_id   int
			      )"""

		cursor.execute(query)

		query="""CREATE TABLE if  not exists user_table(
        	     user_id    int  PRIMARY KEY ,
        	     user_name  varchar(255),
        	     address    varchar(255))"""

		cursor.execute(query)

		return connection


	except mysql.connector.Error as error:

		print("some error occured:",error)

		return "connection not established"
    

@app.route('/to_do_list/<int:usr_id>',methods=["GET"])

def get_to_do_list(usr_id):

	conn=db_connection()

	cur=conn.cursor()

	query="""SELECT * from to_do_list_table1
	         WHERE user_id=%s"""

	cur.execute(query,(usr_id,))

	result=cur.fetchall()

	to_do_list=[
	           {"task_id":row[0],
	           "task_name":row[1],
			    "status":row[2],
			    "category":row[3],
			    "completing_date":row[4],
			    "user_id":row[5]
			   }
			   for row in result]

	cur.close()

	conn.close()

	return (jsonify(to_do_list))

@app.route('/to_do_list/<int:usr_id>',methods=["POST"])

def insert_task(usr_id):

	conn=db_connection()

	cursor=conn.cursor()

	query=""" INSERT INTO to_do_list_table1
	          (task_name,status,category,completing_date,user_id)
	          VALUES(%s,%s,%s,%s,%s)"""


	status_options=["due","completed"]


	category_options=["finance","accounting","health","gardening","studying"]

	task_name=request.form["task_name"]
	status=request.form["status"]
	category=request.form["category"]
	completing_date=request.form["completing_date"]



	if status not in status_options:
		return "this status option not avaliable,please enter valid status in form options avaliable : due , completed"

	if category not in category_options:
		return "this category option not avaliable in form ,please enter valid category in form options avaliable :finance,accounting,health,gardening,studying"

	cursor.execute(query,(task_name,status,category,completing_date,usr_id))

	conn.commit()

	cursor.close()

	conn.close()

	updated_list={
	              "task_name":task_name,
	              "status":status,
	              "category":category,
	              "completing_date":completing_date,
	              "user_id":usr_id
	              }

	return jsonify(updated_list)

@app.route("/to_do_list/<int:usr_id>/<int:id>",methods=["DELETE"])

def delete_task(usr_id,id):

	conn=db_connection()

	cursor=conn.cursor()

	query="""SELECT user_id from to_do_list_table1
	         where user_id=%s"""
    
	cursor.execute(query,(usr_id,))

	result=cursor.fetchone()

	if result is not None:

		query="""SELECT task_id from to_do_list_table1
		         where task_id=%s and user_id=%s"""

		cursor.execute(query,(id,usr_id))

		result=cursor.fetchone()

		print(result)

		if result is not None:

			query="""DELETE FROM to_do_list_table1
			         where user_id=%s and task_id=%s"""

			cursor.execute(query,(usr_id,id))

			conn.commit()

			cursor.close()

			conn.close()

			return "task with task_id {} for user with user_id {} deleted from to_do_list ".format(id,usr_id)

		else:
			return "task with task_id {} for user_id {} doen't exist".format(id,usr_id)

	cursor.close()

	conn.close()

	return "task with task_id for given user_id doesn't exist in your to_do_list"

@app.route("/to_do_list/<int:usr_id>/<int:id>",methods=["PATCH"])

def update_task(usr_id,id):

	conn=db_connection()

	cursor=conn.cursor()

	query="""SELECT user_id from to_do_list_table1
	         where user_id=%s"""

	cursor.execute(query,(usr_id,))

	result=cursor.fetchone()

	if result is not None:

		query="""SELECT task_id from to_do_list_table1
		         where task_id=%s and user_id=%s"""

		cursor.execute(query,(id,usr_id))

		result=cursor.fetchone()

		if result is not None:

			task_name=request.form.get("task_name",default="")

			if task_name:

				query="""UPDATE to_do_list_table1 SET 
				         task_name=%s
				         WHERE user_id=%s and task_id=%s"""


				cursor.execute(query,(task_name,usr_id,id))

				conn.commit()

				cursor.close()

				conn.close()

				return "task updated"

			status=request.form.get("status",default="")

			if status:

				query="""UPDATE to_do_list_table1 SET 
				         status=%s
				         WHERE user_id=%s and task_id=%s"""


				cursor.execute(query,(status,usr_id,id))

				conn.commit()

				cursor.close()

				conn.close()

				return "task updated"

			else:
				return "please enter valid task"
		else:
			return "task id for user_id {} doesn't exist".format(usr_id)

	else:
		return "user id {} not exist".format(usr_id)

@app.route('/user_list',methods=["GET"])

def get_user_info():

	conn=db_connection()

	cur=conn.cursor()

	query="""SELECT * from user_table"""

	cur.execute(query)

	result=cur.fetchall()

	user_information=[
	                  {"user_id":row[0],
	                   "user_name":row[1],
			           "address":row[2]
			          }
			            for row in result]

	cur.close()

	conn.close()

	return jsonify(user_information)

@app.route("/user_list",methods=["POST"])

def insert_user_info():

	conn=db_connection()

	cursor=conn.cursor()

	query="""INSERT INTO user_table 
	         (user_id,user_name,address)
	         VALUES(%s,%s,%s)"""

	user_id=request.form["user_id"]

	user_name=request.form["user_name"]

	address=request.form["address"]

	cursor.execute(query,(user_id,user_name,address))

	user_list={"user_id":user_id,
	           "user_name":user_name,
	           "address":address}

	conn.commit()

	cursor.close()

	conn.close()

	return jsonify(user_list)

@app.route("/user_list/<int:usr_id>",methods=["PATCH"])

def user_info_update(usr_id):

	conn=db_connection()

	cur=conn.cursor()

	query="""UPDATE user_table 
	         SET address=%s
	         WHERE user_id=%s"""

	user_address=request.form["address"]

	user_id=usr_id

	cur.execute(query,(user_address,user_id))

	conn.commit()

	cur.close()

	conn.close()

	return "user_info updated"



if __name__=="__main__":

	app.run(debug=True)
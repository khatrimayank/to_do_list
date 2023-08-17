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

		return connection


	except mysql.connector.Error as error:

		print("some error occured:",error)

		return jsonify(error="connection not established"),500

def validate_user_id(user_id):
	
	conn=db_connection()

	cursor=conn.cursor()

	query="""SELECT user_id from to_dos
	         WHERE user_id=%s"""

	cursor.execute(query,(user_id,))

	result=cursor.fetchone()

	if result is not None:
		return result

	else:
		return None


def validate_task_id(id,user_id):
	
	conn=db_connection()

	cursor=conn.cursor()

	query="""SELECT task_id from to_dos
	         WHERE task_id=%s and user_id=%s"""

	cursor.execute(query,(id,user_id))

	result=cursor.fetchone()

	if result is not None:
		return result

	else:
		return None


@app.route('/tasks/api/v1/<int:id>',methods=["GET"])

def get_tasks(id):

	conn=db_connection()

	cur=conn.cursor()

	query="""SELECT * from to_dos
	         WHERE task_id=%s and user_id=%s"""

	user_id=request.headers.get("user_id")

	res=validate_user_id(user_id)

	if res is None:
		return jsonify("authentication error:user id not exist"),401

	res=validate_task_id(id,user_id)

	if res is None:
		return jsonify("Not Found error:task id not fond"),404

	cur.execute(query,(id,user_id))

	result=cur.fetchall()

	to_dos=[
	           {"task_id":row[0],
	           "task_name":row[1],
			    "status":row[2],
			    "category":list(row[3]),
			    "completing_date":row[4],
			    "user_id":row[5]
			   }
			   for row in result]

	cur.close()

	conn.close()

	return jsonify(to_dos),200

@app.route('/tasks/api/v1',methods=["GET"])

def get_all_tasks():

	conn=db_connection()

	cur=conn.cursor()

	query="""SELECT * from to_dos
	         Where user_id=%s"""

	user_id=request.headers.get("user_id")


	res=validate_user_id(user_id)

	if not res:
		return jsonify("authentication error:user id not exist"),401

	cur.execute(query,(user_id,))

	result=cur.fetchall()

	to_dos=[
	           {"task_id":row[0],
	           "task_name":row[1],
			    "status":row[2],
			    "category":list(row[3]),
			    "completing_date":row[4],
			    "user_id":row[5]
			   }
			   for row in result]

	cur.close()

	conn.close()

	return (jsonify(to_dos)),200

@app.route('/tasks/api/v1',methods=["POST"])

def insert_task():

	conn=db_connection()

	cursor=conn.cursor()

	query=""" INSERT INTO to_dos
	          (task_name,status,category,completing_date,user_id)
	          VALUES(%s,%s,%s,%s,%s)"""

	status_options=["due","completed"]

	category_options=["finance","accounting","health","gardening","studying"]

	user_id=request.headers.get("user_id")
	task_name=request.form["task_name"]
	status=request.form["status"]
	category=request.form["category"]
	completing_date=request.form["completing_date"]

	if status not in status_options:
		return jsonify("this status option not avaliable,please enter valid status in form options avaliable : due , completed"),400

	if len(category.split(","))!=0:
		for item in (category.split(",")) :
			if item not in category_options:
				return jsonify("this category option not avaliable,please enter valid category in form options avaliable"),400               

	else:
		return jsonify("this category option not avaliable,please enter valid category in form options avaliable"),400

	cursor.execute(query,(task_name,status,category,completing_date,user_id))

	conn.commit()

	cursor.close()

	conn.close()

	updated_list={
	              "task_name":task_name,
	              "status":status,
	              "category":category,
	              "completing_date":completing_date,
	              "user_id":user_id
	              }

	return jsonify(updated_list),201

@app.route("/tasks/api/v1/<int:id>",methods=["DELETE"])

def delete_task(id):

	conn=db_connection()

	cursor=conn.cursor()

	user_id=request.headers.get("user_id")

	res=validate_user_id(user_id)

	if not user_id:
		return jsonify("authentication error:user_id not exists"),401

	res=validate_task_id(id,user_id)

	if not res: 
		return jsonify("data not found:for given user id,task id not found"),404


	query="""DELETE FROM to_dos
		     Where task_id=%s and user_id=%s"""

	cursor.execute(query,(id,user_id))

	conn.commit()

	cursor.close()

	conn.close()

	return jsonify("task with task_id {} for user_id {} deleted from to_do_list ".format(id,user_id)),201

@app.route("/tasks/api/v1/<int:id>",methods=["PATCH"])

def update_task(id):

	conn=db_connection()

	cursor=conn.cursor()

	user_id=request.headers.get("user_id")
    
	res=validate_user_id(user_id)

	if not res:
		return jsonify("authentication error:user_id not exists"),401

	res=validate_task_id(id,user_id)

	if not res:
		return jsonify("data not found:for given user id,task id not found"),404

	task_name=request.form.get("task_name",default="")

	if task_name:
		query="""UPDATE to_dos SET 
		         task_name=%s
		         WHERE user_id=%s and task_id=%s"""

		cursor.execute(query,(task_name,user_id,id))

		conn.commit()

		cursor.close()

		conn.close()

		return jsonify("task updated:task_name for given task_id and user_id updated"),201

		status=request.form.get("status",default="")

		if status:
			query="""UPDATE to_dos SET 
			         status=%s
			         WHERE user_id=%s and task_id=%s"""

			cursor.execute(query,(status,user_id,id))

			conn.commit()

			cursor.close()

			conn.close()

			return jsonify("task updated:status for given task_id and user_id updated"),201

@app.route('/users/api/v1',methods=["GET"])

def get_user_info():

	conn=db_connection()

	cur=conn.cursor()

	query="""SELECT * from users"""

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

	return jsonify(user_information),200

@app.route("/users/api/v1",methods=["POST"])

def insert_user_info():

	conn=db_connection()

	cursor=conn.cursor()

	query="""INSERT INTO users 
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

	return jsonify(user_list),201

@app.route("/users/api/v1/<int:usr_id>",methods=["PATCH"])

def user_info_update(usr_id):

	conn=db_connection()

	cur=conn.cursor()

	query="""UPDATE users
	         SET address=%s
	         WHERE user_id=%s"""

	user_address=request.form.get("address",default="")

	user_id=usr_id

	query="""SELECT user_id from users
	         WHERE user_id=%s"""

	cur.execute(query,(usr_id))

	res=cur.fetchone()

	if not res:
		return jsonify("not found error:user id not found"),404

	cur.execute(query,(address,user_id))

	conn.commit()

	cur.close()

	conn.close()

	return jsonify("user_info updated:address updated"),201


if __name__=="__main__":

	app.run(debug=True)

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow import ValidationError
import mysql.connector
from mysql.connector import Error

db_name=" gym_db"
user="root"
password="S05071984"
host="127.0.0.1"

try:
    def get_db_connection():
        conn=mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
    
)
        if conn.is_connected():
            print("MySQL database is connected successfully")
        
   
except ValueError as e:
    print(f'Error: {e}')


app = Flask(__name__)
ma=Marshmallow(app)

class WorkoutSchema(ma.Schema):
    session_id=fields.Integer(required=True)
    member_id=fields.Integer(required=True)
    session_date=fields.Date(required=True)
    session_time=fields.String(required=True)
    activity=fields.String(required=True)
    
    class Meta:
        fields=("session_id", "member_id","session_date", "session_time", "activity")

session_schema=WorkoutSchema()
sessions_schema=WorkoutSchema(many=True)

@app.route('/')
def hello_world():
   return 'Welcome To Gym Management System (Flask)'

@app.route('/workoutsessions', methods=['GET'])
def get_session():
    try:
        conn=mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
    
)
        if conn is None:
            return jsonify({"Error:"}),500
        cursor=conn.cursor(dictionary=True)
        query= " SELECT * FROM workoutsessions"
        cursor.execute(query)
        customers=cursor.fetchall()
        return sessions_schema.jsonify(customers)
    except Error as e:
        print(f"Error:{e}")
        return({"Error Internal"}),500
        
    finally:
        print("Database is connected")
        
@app.route('/workoutsessions', methods=['POST']) #http://127.0.0.1:5000/members
def add_session():
    
    try:
        session_data=session_schema.load(request.json)
    except Error as e:
        print(f"Error{e}")
        return jsonify (e.message),400
    
    try:
        conn=get_db_connection()
        conn=mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
            
    
)
        if conn is None:
            return jsonify ({"Error: Database connection failed"}),500
        
        cursor=conn.cursor(dictionary=True)
        new_session=(session_data['session_id'], session_data['member_id'], session_data['session_time'],session_data['activity'])
        query=" INSERT INTO workoutsessions (session_id, member_id, session_date, session_time, activity) VALUES ( %s, %s, %s, %s, %s)"
        cursor.execute(query,new_session)
        conn.commit()
        return jsonify({"message":"New session added successfully"}), 201
        
    except Error as e:
        print(f" Error:{e}")
        return jsonify ({"Error":" Internal Server Error"}),500
       
    finally:
        print("Database Status: Currently Connected")
       
        
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
    
    
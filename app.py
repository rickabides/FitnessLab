import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime
from tg_helper import TigerGraphHelper 

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Assuming you have these credentials and connection details
HOST = "https://0560bfbf6f6f420999a20420a6208cfa.i.tgcloud.io/"
GRAPH_NAME = "FitnessClasses"
USERNAME = "user_3"
PASSWORD = "YOURPASS"
SECRET = 'APISECRET'

tg_helper = TigerGraphHelper(host=HOST, graphname=GRAPH_NAME, username=USERNAME, password=PASSWORD, secret=SECRET)

@app.route('/')
def index():
    # Render the main index page
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    age = request.form['age']
    gender = request.form['gender']
    join_date = datetime.now()  # Assume current time as join date
    membership_level = request.form['membership_level']
    weight = request.form.get('weight', 0) # if empty enter 0
    
    result, membership_id = tg_helper.create_user(age, gender, join_date, membership_level, weight)

    # Return the entire result along with specific details
    return jsonify({
        "success": True,
        "message": "User created",
        "Membership_ID": membership_id,
        "data": result})
 
@app.route('/create_class', methods=['POST'])
def create_class():
    category = request.form['category']
    difficulty_level = int(request.form['difficulty_level'])
    name = request.form['name']
    typical_duration = int(request.form['typical_duration'])
    result = tg_helper.create_class(category, difficulty_level, name, typical_duration)
    return jsonify({"success": True, "message": "Class created", "data": result})

@app.route('/create_session', methods=['POST'])
def create_session():
    class_id = request.form['class_id']
    capacity = int(request.form['capacity'])
    room = request.form['room']
    specific_date = datetime.strptime(request.form['specific_date'], '%Y-%m-%d')
    
    start_time = str(request.form['start_time'])
    end_time = str(request.form['end_time'])
    
    result, session_id = tg_helper.create_session(class_id, capacity, room, specific_date, start_time, end_time)
    return jsonify({
        "success": True,
         "message": "Session created",
         "session_id": session_id,
         "data": result})

@app.route('/register', methods=['POST'])
def register():
    user_id = request.form['user_id']
    session_id = request.form['session_id']
    result = tg_helper.register_user_for_session(user_id, session_id)
    return jsonify({"success": True, "message": "Registration successful", "data": result})

@app.route('/cancel_registration', methods=['POST'])
def cancel_registration():
    user_id = request.form['user_id']
    session_id = request.form['session_id']

    if not user_id or not session_id:
        return jsonify({"success": False, "message": "User ID and Session ID are required"}), 400

    try:
        result = tg_helper.cancel_user_registration(user_id, session_id)
        if result:
            return jsonify({"success": True, "message": "Registration canceled successfully"})
        else:
            return jsonify({"success": False, "message": "Failed to cancel registration"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

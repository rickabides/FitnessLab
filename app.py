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
PASSWORD = ""
SECRET = ''

tg_helper = TigerGraphHelper(host=HOST, graphname=GRAPH_NAME, username=USERNAME, password=PASSWORD, secret=SECRET)

@app.route('/')
def index():
    # Render the main index page
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        user_data = {
            'age': request.form['age'],
            'gender': request.form['gender'],
            'join_date': datetime.now(),
            'membership_level': request.form['membership_level'],
            'weight': request.form.get('weight', 0)
        }
        result, membership_id = tg_helper.create_user(**user_data)
        return jsonify({"success": True, "message": "User created", "Membership_ID": membership_id})
    except KeyError as e:
        return jsonify({"success": False, "message": f"Missing parameter: {e}"}), 400
 
@app.route('/create_class', methods=['POST'])
def create_class():
    category = request.form['category']
    difficulty_level = int(request.form['difficulty_level'])
    name = request.form['name']
    typical_duration = int(request.form['typical_duration'])
    # Assuming 'create_class' in 'TigerGraphHelper' returns success status and class name or ID
    result, class_id = tg_helper.create_class(category, difficulty_level, name, typical_duration)
    return jsonify({"success": True, "message": "Class created", "data": {"Name": name, "Class_ID": class_id}})

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

@app.route('/create_instructor', methods=['POST'])
def create_instructor():
    name = request.form['name']
    specialization = request.form['specialization']
    years_of_experience = request.form['years_of_experience']
    # Assuming 'create_instructor' in 'TigerGraphHelper' handles the creation logic
    result, instructor_id = tg_helper.create_instructor(name, specialization, int(years_of_experience))
    return jsonify({"success": True, "message": "Instructor created", "data": {"Name": name, "Instructor_ID": instructor_id}})

@app.route('/register', methods=['POST'])
def register():
    user_id = request.form['user_id']
    session_id = request.form['session_id']
    result = tg_helper.register_user_for_session(user_id, session_id)
    return jsonify({"success": True, "message": "Registration successful", "data": result})

@app.route('/cancel_registration', methods=['POST'])
def cancel_registration():
    user_id = request.form.get('user_id')
    session_id = request.form.get('session_id')
    if not user_id or not session_id:
        return jsonify({"success": False, "message": "User ID and Session ID are required"}), 400
    success = tg_helper.cancel_user_registration(user_id, session_id)
    return jsonify({"success": success, "message": "Cancelled successfully" if success else "Cancellation failed"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

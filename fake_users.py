import requests
import random
from faker import Faker
from datetime import datetime, timedelta
import json

# Initialize Faker to generate fake data
fake = Faker()

# Base URL of your Flask app
BASE_URL = "http://localhost:8080"

# Set up the log file
LOG_FILE = "flask_app_responses.log"

def log_response(data):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

def create_fake_user():
    user_data = {
        'age': random.randint(18, 70),
        'gender': random.choice(['Male', 'Female', 'Other']),
        'join_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'membership_level': random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']),
        'weight': random.randint(50, 120)
    }
    response = requests.post(f"{BASE_URL}/signup", data=user_data)
    response_json = response.json()
    log_response(response_json)
    return response_json

def create_fake_class():
    class_data = {
        'category': random.choice(['Yoga', 'Pilates', 'Zumba', 'Weightlifting']),
        'difficulty_level': random.randint(1, 5),
        'name': fake.word().capitalize(),
        'typical_duration': random.randint(30, 120)  # Duration in minutes
    }
    response = requests.post(f"{BASE_URL}/create_class", data=class_data)
    response_json = response.json()
    log_response(response_json)
    return response_json

def create_fake_session(class_id):
    session_data = {
        'class_id': class_id,
        'capacity': random.randint(5, 30),
        'room': f"Room {random.randint(1, 10)}",
        'specific_date': (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
        'start_time': '10:00',
        'end_time': '11:00'
    }
    response = requests.post(f"{BASE_URL}/create_session", data=session_data)
    response_json = response.json()
    log_response(response_json)
    return response_json

def create_fake_instructor():
    instructor_data = {
        'name': fake.name(),
        'specialization': random.choice(['Yoga', 'Pilates', 'Cardio', 'Strength Training', 'Dance']),
        'years_of_experience': random.randint(1, 20)
    }
    response = requests.post(f"{BASE_URL}/create_instructor", data=instructor_data)
    response_json = response.json()
    log_response(response_json)
    return response_json

def main():
    # Create multiple users
    print("Creating Users:")
    for _ in range(5):  # Adjust the range as needed
        user = create_fake_user()
        print(user)
    
    # Create multiple classes
    class_ids = []
    for _ in range(2):  # Adjust the range as needed
        class_info = create_fake_class()
        if class_info['success']:
            class_ids.append(class_info['data']['Name'])
            print(f"Class ID: {class_info['data']['Class_ID']}")  # Example if 'Class_ID' is part of the response

        else:
            print(f"Failed to create class: {class_info['message']}")

    # Create multiple sessions
    print("\nCreating Sessions:")
    for class_id in class_ids:
        session = create_fake_session(class_id)
        print(session)

    # Create multiple instructors
    print("\nCreating Instructors:")
    for _ in range(3):  # Adjust the range as needed
        instructor = create_fake_instructor()
        if instructor['success']:
            print(f"Instructor created successfully: {instructor}")
        else:
            print(f"Failed to create instructor: {instructor['message']}")


if __name__ == "__main__":
    main()

import requests
import random

# Configuration
BASE_URL = "http://localhost:8080"

# Sample data: Replace these with functions to fetch real data if needed
members = ['aec60314-f6d9-4b76-9fbe-83b0f71dc37a', 'eca90bdf-6fde-42f1-9940-245b94527bc3', '35171d05-f9de-4e74-86f3-e93c0201ab5a', '05af449a-5341-43e3-b846-cb9d71592dd7', 'a62ece2c-ed71-4f5a-a41d-eea1d86cfca2', '17633a3c-eaa5-462a-82d6-debcc56e9bf2']
sessions = ['Every_20240530', 'Argue_20240519', 'Point_20240521', 'Trip_20240517']

def register_member_to_session(member_id, session_id):
    """ Registers a member to a session """
    response = requests.post(f"{BASE_URL}/register", data={'user_id': member_id, 'session_id': session_id})
    return response.json()

def cancel_member_registration(member_id, session_id):
    """ Cancels a member's registration for a session """
    response = requests.post(f"{BASE_URL}/cancel_registration", data={'user_id': member_id, 'session_id': session_id})
    return response.json()

def simulate_registrations(members, sessions):
    """ Simulate random registrations """
    registrations = []
    for member in members:
        session = random.choice(sessions)
        result = register_member_to_session(member, session)
        print(f"Registration result for {member} to {session}: {result}")
        if result.get('success', False):
            registrations.append((member, session))
    return registrations

def simulate_cancellations(registrations):
    """ Simulate random cancellations from existing registrations """
    to_cancel = random.sample(registrations, k=len(registrations)//2)  # Cancel about half of the registrations
    for member, session in to_cancel:
        result = cancel_member_registration(member, session)
        print(f"Cancellation result for {member} from {session}: {result}")

def main():
    # Simulate registrations
    registrations = simulate_registrations(members, sessions)
    
    # Simulate cancellations
    simulate_cancellations(registrations)

if __name__ == '__main__':
    main()


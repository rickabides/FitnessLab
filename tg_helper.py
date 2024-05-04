import uuid
import pyTigerGraph as tg
from datetime import datetime

class TigerGraphHelper:
    def __init__(self, host, graphname, username, password, secret):
        self.conn = tg.TigerGraphConnection(host=host, graphname=graphname, username=username, password=password)
        self.conn.getToken(secret)

    def create_user(self, age, gender, join_date, membership_level, weight):
        membership_id = uuid.uuid4()
        attributes = {
            "Age": int(age),
            "Gender": gender,
            "Join_Date": join_date.strftime('%Y-%m-%d %H:%M:%S'),
            "Membership_Level": membership_level,
            "Weight": int(weight),
            "Membership_ID": str(membership_id)
        }
        result = self.conn.upsertVertex("User", str(membership_id), attributes)
        return result, str(membership_id)

#    def create_class(self, category, difficulty_level, name, typical_duration):
#        attributes = {
#            "Category": category,
#            "Difficulty_Level": int(difficulty_level),
#            "Name": name,
#            "Typical_Duration": int(typical_duration)
#        }
#        return self.conn.upsertVertex("Class", name, attributes)
    def create_class(self, category, difficulty_level, name, typical_duration):
        attributes = {
            "Category": category,
            "Difficulty_Level": difficulty_level,
            "Name": name,
            "Typical_Duration": typical_duration
        }
        result = self.conn.upsertVertex("Class", name, attributes)
        return result, name  # Return both the result and the class name or ID


    def create_session(self, class_id, capacity, room, specific_date, start_time, end_time):
        attributes = {
            "Capacity": int(capacity),
            "Current_Enrollment": 0,  # Assuming you need to set this initially
            "Room": room,
            "Specific_Date": specific_date.strftime('%Y-%m-%d'),
            "Start_Time": start_time,
            "End_Time": end_time
        }
        session_id = f"{class_id}_{specific_date.strftime('%Y%m%d')}"
        result = self.conn.upsertVertex("Session", session_id, attributes)
        return result, session_id

    def register_user_for_session(self, user_id, session_id):
        # Edge 'registers_for' from User to Session
        attributes = {
            "Attendance_Status": "Registered",
            "Registration_Date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return self.conn.upsertEdge("User", user_id, "registers_for", "Session", session_id, attributes)

    def cancel_user_registration(self, user_id, session_id):
        try:
            result = self.conn.delEdges(sourceVertexType="User", sourceVertexId=user_id, edgeType="registers_for", targetVertexType="Session", targetVertexId=session_id)
            if 'results' in result and result['results'] and 'deleted_edges' in result['results'][0]:
                return result['results'][0]['deleted_edges'] > 0
            return False
        except Exception as e:
            print(f"Error in cancelling registration: {str(e)}")
            return False

    def create_instructor(self, name, specialization, years_of_experience):
        instructor_id = name.replace(" ", "_") + str(years_of_experience)  # Create a unique ID
        attributes = {
            "Name": name,
            "Specialization": specialization,
            "Years_of_Experience": years_of_experience
        }
        result = self.conn.upsertVertex("Instructor", instructor_id, attributes)
        return result, instructor_id

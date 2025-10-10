import requests
import json
import time
from datetime import datetime

BASE_URL = "http://api_gateway:5000/alarms"

# ---- 1. Add a new alarm ----
new_alarm = {
    "user_id": 1,
    "message": "Wake up",
    "time": datetime.now().isoformat()
}

response = requests.post(f"{BASE_URL}", json=new_alarm)
print("Create Alarm:", response.json())

time.sleep(1)


# ---- 3. Get alarms for a specific user ----
user_id = 1
response = requests.get(f"{BASE_URL}", params={"user_id": user_id})
print(f"Alarms for user {user_id}:", response.json())

# # # ---- 2. List all alarms ----
# # response = requests.get(BASE_URL)
# # print("All Alarms:", response.json())

# # ---- 3. Get alarms for a specific user ----
# user_id = 1
# response = requests.get(f"{BASE_URL}/user/{user_id}")
# print(f"Alarms for user {user_id}:", response.json())

# ---- 4. Get a specific alarm by ID ----
alarm_id = 1
response = requests.get(f"{BASE_URL}/{alarm_id}")
print(f"Alarm {alarm_id}:", response.json())

# # ---- 5. Update an alarm ----
# updated_alarm = {
#     "user_id": 1,
#     "message": "Updated wake up time",
#     "time": "2025-10-06T09:00:00"
# }
# response = requests.put(f"{BASE_URL}/{alarm_id}", json=updated_alarm)
# print(f"Updated Alarm {alarm_id}:", response.json())

# response = requests.get(f"{BASE_URL}/{alarm_id}")
# print("GET after UPDATE Alarm:", response.json())


# # ---- 6. Delete an alarm ----
# response = requests.delete(f"{BASE_URL}/{alarm_id}")
# print(f"Deleted Alarm {alarm_id}:", response.json())


# response = requests.get(f"{BASE_URL}/{alarm_id}")
# print("GET after DELETE Alarm:", response.json())

# user_id = 1
# response = requests.get(f"{BASE_URL}/user/{user_id}")
# print(f"Alarms for user {user_id}:", response.json())


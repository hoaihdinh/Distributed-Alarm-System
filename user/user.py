import requests
import json

BASE_URL = "http://api_gateway:5000/alarms"

# ---- 1. Add a new alarm ----
new_alarm = {
    "message": "Wake up",
    "time": "2025-10-06T08:00:00"
}
user_id = 1

response = requests.post(f"{BASE_URL}/{user_id}", json=new_alarm)

try:
    data = response.json()
except ValueError:  # requests.JSONDecodeError is subclass of ValueError
    data = {"raw_text": response.text or "No content"}

print("Create Alarm:", data)

# # ---- 2. List all alarms ----
# response = requests.get(BASE_URL)
# print("All Alarms:", response.json())

# ---- 3. Get alarms for a specific user ----
response = requests.get(f"{BASE_URL}/user/{user_id}")
print(f"Alarms for user {user_id}:", response.json())

# ---- 4. Get a specific alarm by ID ----
alarm_id = 1
response = requests.get(f"{BASE_URL}/{alarm_id}")
print(f"Alarm {alarm_id}:", response.json())

# ---- 5. Update an alarm ----
updated_alarm = {
    "user_id": 1,
    "message": "Updated wake up time",
    "time": "2025-10-06T09:00:00"
}
response = requests.put(f"{BASE_URL}/{alarm_id}", json=updated_alarm)
print(f"Updated Alarm {alarm_id}:", response.json())

# ---- 6. Delete an alarm ----
response = requests.delete(f"{BASE_URL}/{alarm_id}")
print(f"Deleted Alarm {alarm_id}:", response.json())

import requests

ALARM_URL = "http://alarm_manager:5001/alarms"

def delete_alarms_for_user(user_id: int):
    response = requests.delete(f"{ALARM_URL}", params={"user_id": user_id})
    if not response.ok:
        print(f"[Warning] Failed to delete alarms for user {user_id}: {response.status_code}")
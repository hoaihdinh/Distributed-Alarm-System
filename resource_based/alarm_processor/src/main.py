import requests
import time
from datetime import datetime

ALARM_URL = "http://alarm_storage:5001/alarms"

POLL_INTERVAL = 0.01 # 10ms of time

while True:
    try:
        response = requests.get(f"{ALARM_URL}/pending")
        pending_alarms = response.json()

        for alarm in pending_alarms:
            alarm_time = datetime.fromisoformat(alarm["time"])

            if alarm_time <= datetime.now():
                
                # Publish Notification (POST)

                requests.put(f"{ALARM_URL}/{alarm['id']}", json={"status": "notified"})
                
        time.sleep(POLL_INTERVAL)
    
    except Exception as e:
        print("Scheduler error:", e)
        time.sleep(POLL_INTERVAL)

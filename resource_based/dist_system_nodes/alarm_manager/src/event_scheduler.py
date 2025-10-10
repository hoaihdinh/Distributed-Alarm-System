from datetime import datetime
import requests

SCHEDULER_URL = "http://scheduler:5002/events"

def create_event(alarm_id: int, time: datetime):
    requests.post(f"{SCHEDULER_URL}/{alarm_id}", json={"time": time.isoformat()})

def update_event(alarm_id: int, time: datetime):
    requests.put(f"{SCHEDULER_URL}/{alarm_id}", json={"time": time.isoformat()})

def delete_event(alarm_id: int):
    requests.delete(f"{SCHEDULER_URL}/{alarm_id}")
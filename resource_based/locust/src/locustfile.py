from locust import HttpUser, task, between, events
import random
import gevent
from datetime import datetime, timedelta, timezone

class APIUser(HttpUser):
    wait_time = between(1, 3)  # simulate user think time

    def fetch_alarms(self):
        while True:
            with self.client.get(f"/alarms?user_id={self.user_id}", catch_response=True) as response:
                self.handle_response(response, "Get Alarm Request")
            gevent.sleep(0.5)
    
    def fetch_notifications(self):
        while True:
            with self.client.get(f"/notifications?user_id={self.user_id}", catch_response=True) as response:
                if self.handle_response(response, "Get Notification Request"):
                    notifs = response.json()
                    self.notifications = [notif["id"] for notif in notifs]
            gevent.sleep(0.5)

    def on_start(self):
        self.user_id = None

        # Create a new user
        username = f"user_{random.randint(1, 100000)}"
        password = "password123"

        # Keep looping until logged in
        while self.user_id is None:
            with self.client.post(
                "/users/register",
                json={"username": username, "password": password},
                catch_response=True
            ) as response:    
                if response.status_code in (200, 201):
                    self.user_id = response.json()["id"]
                    self.username = username
                    self.password = password
                    response.success()
                elif response.status_code == 409:
                    with self.client.post(
                        "/users/authenticate",
                        json={"username": username, "password": password},
                        catch_response=True
                    ) as response:
                        if response.status_code in (200, 201):
                            self.user_id = response.json()["id"]
                            response.success()
                        else:
                            response.failure(f"Failed to authenticate user {username}: {response.status_code}")
                else:
                    response.failure(f"Failed to register user {username}: {response.status_code}")

            gevent.sleep(1)

        # store alarm and notification IDs created during this session
        self.alarms = []
        self.notifications = []
        self.create_alarm()
        # Simulate frontend polling to get notifications and alarms
        gevent.spawn(self.fetch_alarms)
        gevent.spawn(self.fetch_notifications)

    def random_alarm_time(self):
        now = datetime.now(timezone.utc)
        delta = timedelta(minutes=random.randint(1, 5))
        return (now + delta).isoformat()

    def handle_response(self, response, name="Request"):
        if response.status_code in (200, 201):
            response.success()
            return True
        else:
            response.failure(f"{name} failed with status {response.status_code}: {response.text}")
            return False

    @task(8)
    def create_alarm(self):
        alarm_time = self.random_alarm_time()
        message = f"Test Alarm for user {self.user_id}"
        
        with self.client.post(
            "/alarms",
            json={
                "user_id": self.user_id,
                "time": alarm_time,
                "message": message,
                "status": "pending"
            },
            catch_response=True
        ) as response:
            if self.handle_response(response, "Create Alarm Request"):
                alarm_id = response.json().get("id")
                if alarm_id:
                    self.alarms.append(alarm_id)

    @task(5)
    def delete_specific_alarm(self):
        if self.alarms:
            alarm_id = random.choice(self.alarms)
            with self.client.delete(f"/alarms/{alarm_id}", catch_response=True) as response:
                if self.handle_response(response, "Delete Alarm Request"):
                    self.alarms.remove(alarm_id)

    @task(5)
    def update_alarm(self):
        if self.alarms:
            alarm_id = random.choice(self.alarms)
            new_message = f"Updated Alarm for user {self.user_id} [{random.randint(1, 100000)}]"
            alarm_time = self.random_alarm_time()

            with self.client.put(
                f"/alarms/{alarm_id}",
                json={
                    "message": new_message,
                    "time": alarm_time
                },
                catch_response=True
            ) as response:
                self.handle_response(response, "Update Alarm Request")
                
    @task(5)
    def delete_notification(self):
        if self.notifications:
            notification_id = random.choice(self.notifications)
            with self.client.delete(f"/notifications/{notification_id}", catch_response=True) as response:
                if self.handle_response(response, "Delete Notification Request"):
                    self.notifications.remove(notification_id)


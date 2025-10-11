from locust import HttpUser, task, between
import random

class APIUser(HttpUser):
    wait_time = between(1, 3)  # simulate user think time

    def on_start(self):
        """Run once per simulated user at start."""
        # Create a new user
        username = f"user_{random.randint(1, 100000)}"
        password = "password123"
        response = self.client.post("/users/register", json={"username": username, "password": password})
        if response.status_code in (200, 201):
            self.user_id = response.json()["id"]
            self.username = username
            self.password = password
        else:
            # fallback: try authenticate existing user
            response = self.client.post("/users/authenticate", json={"username": username, "password": password})
            if response.status_code == 200:
                self.user_id = response.json()["id"]
            else:
                self.user_id = None

        # store alarm IDs created during this session
        self.alarms = []

    @task(8)
    def create_alarm(self):
        if not hasattr(self, "user_id") or self.user_id is None:
            return
        alarm_time = "2025-10-10T18:00:00"
        message = f"Test Alarm {random.randint(1, 100000)}"
        response = self.client.post("/alarms", json={
            "user_id": self.user_id,
            "time": alarm_time,
            "message": message,
            "status": "pending"
        })
        if response.status_code in (200, 201):
            alarm_id = response.json().get("id")
            if alarm_id:
                self.alarms.append(alarm_id)

    @task(2)  # delete all alarms (rare)
    def delete_all_alarms(self):
        if hasattr(self, "user_id") and self.user_id is not None:
            self.client.delete(f"/alarms?user_id={self.user_id}")
            self.alarms.clear()

    @task(5)  # delete a specific alarm
    def delete_specific_alarm(self):
        if self.alarms:
            alarm_id = random.choice(self.alarms)
            response = self.client.delete(f"/alarms/{alarm_id}")
            if response.status_code == 200:
                self.alarms.remove(alarm_id)

    @task(5)
    def update_alarm(self):
        if self.alarms:
            alarm_id = random.choice(self.alarms)
            new_message = f"Updated Alarm {random.randint(1, 100000)}"
            self.client.put(f"/alarms/{alarm_id}", json={
                "message": new_message
            })

    @task(10)
    def get_alarms(self):
        if hasattr(self, "user_id") and self.user_id is not None:
            self.client.get(f"/alarms?user_id={self.user_id}")

    @task(10)
    def sse_test(self):
        if hasattr(self, "user_id") and self.user_id is not None:
            with self.client.get(f"/notifications/stream?user_id={self.user_id}", stream=True, catch_response=True) as response:
                try:
                    for i, line in enumerate(response.iter_lines()):
                        if i >= 3:
                            break
                except Exception:
                    pass

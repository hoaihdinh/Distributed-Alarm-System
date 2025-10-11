from locust import HttpUser, task, between, events
import random
import time
import gevent
from datetime import datetime, timedelta, timezone

class APIUser(HttpUser):
    wait_time = between(1, 3)  # simulate user think time

    def random_alarm_time(self):
        now = datetime.now(timezone.utc)
        delta = timedelta(minutes=random.randint(1, 5))
        return (now + delta).isoformat()

    def open_sse_connection(self):
        while True:
            try:
                with self.client.get(
                    f"/notifications/stream?user_id={self.user_id}",
                    stream=True,
                    timeout=None,
                    catch_response=True
                ) as resp:
                    resp.success()
                    for line in enumerate(resp.iter_lines(decode_unicode=True)):
                        gevent.sleep(0)  # yield to other greenlets
            except Exception as e:
                events.request_failure.fire(
                    request_type="GET",
                    name="/notifications/stream",
                    response_time=0,
                    exception=e
                )

            gevent.sleep(1)  # backoff before reconnecting

    def on_start(self):
        """Run once per simulated user at start."""
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
                if response.ok:
                    self.user_id = response.json()["id"]
                    self.username = username
                    self.password = password
                elif response.status_code == 409:
                    with self.client.post(
                        "/users/authenticate",
                        json={"username": username, "password": password},
                        catch_response=True
                    ) as response:
                        if response.ok:
                            self.user_id = response.json()["id"]
                            response.success()
                        else:
                            response.failure(f"Failed to authenticate user {username}: {response.status_code}")
                else:
                    response.failure(f"Failed to register user {username}: {response.status_code}")

            time.sleep(1)

        # store alarm IDs created during this session
        self.alarms = []
        self.create_alarm()
        gevent.spawn(self.open_sse_connection)

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
            if response.ok:
                alarm_id = response.json().get("id")
                if alarm_id:
                    self.alarms.append(alarm_id)
                response.success()
            else:
                response.failure(f"Failed to create alarm for user {self.user_id}: {response.status_code}")

    @task(5)
    def delete_specific_alarm(self):
        if self.alarms:
            alarm_id = random.choice(self.alarms)
            with self.client.delete(f"/alarms/{alarm_id}", catch_response=True) as response:
                if response.ok:
                    self.alarms.remove(alarm_id)
                    response.success()
                else:
                    response.failure(f"Failed to delete alarm {alarm_id}: {response.status_code}")

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
                if response.ok:
                    response.success()
                else:
                    response.failure(f"Failed to update alarm {alarm_id}: {response.status_code}")

    @task(10)
    def get_alarms(self):
        with self.client.get(f"/alarms?user_id={self.user_id}", catch_response=True) as response:
            if response.ok:
                response.success()
            else:
                response.failure(f"Failed to fetch alarms under user {self.user_id}")




# Notification node/service client only
# will handle creating the notifications ?
# not sure what this will look like with the api tho


import grpc
from google.protobuf import empty_pb2

import alarm_pb2
import alarm_pb2_grpc


def run_notification_client():
    scheduler_channel = grpc.insecure_channel('localhost:50052')
    scheduler_stub = alarm_pb2_grpc.SchedulerStub(scheduler_channel)
    while True:
        alarm = scheduler_stub.FwdDueAlarm(empty_pb2.Empty())  # blocks until alarm is due
        print(f"Alarm triggered: ID={alarm.id}, Title={alarm.title}")

if __name__ == "__main__":
    run_notification_client()
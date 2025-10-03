
# testing storage and scheduler nodes
# run both node 1 and 2 before this


import grpc
import time
from google.protobuf import empty_pb2
import alarm_pb2
import alarm_pb2_grpc

# Connect to storage server
storage_channel = grpc.insecure_channel('localhost:50051')
storage_stub = alarm_pb2_grpc.StorageStub(storage_channel)
# connect to scheduler server 
scheduler_channel = grpc.insecure_channel('localhost:50052')
scheduler_stub = alarm_pb2_grpc.SchedulerStub(scheduler_channel)

# List alarms 
print("Listing alarms before:")
for a in storage_stub.ListAlarms(empty_pb2.Empty()):
    print(f" - ID={a.id}, Title={a.title}")

# Schedule an alarm for 5 secs in the future
trigger_time = int(time.time()) + 5
alarm = alarm_pb2.Alarm(
    id=0,
    title="Wake up in 5 seconds",
    time={"seconds": trigger_time}  # timestamp in seconds
)
scheduler_stub.ScheduleAlarm(alarm)
print(f"Scheduled alarm for {trigger_time}")

# schedule alarm for 10 secs in future
trigger_time = int(time.time()) + 10
alarm = alarm_pb2.Alarm(
    id=0,
    title="Wake up in 10 seconds",
    time={"seconds": trigger_time}  
)
scheduler_stub.ScheduleAlarm(alarm)
print(f"Scheduled alarm for {trigger_time}")


# test receiving a due alarm
resp = scheduler_stub.FwdDueAlarm(empty_pb2.Empty())  # will block
print(f"Received due alarm: ID={resp.id}, Title={resp.title}")

# List alarms 
print("Listing alarms after:")
for a in storage_stub.ListAlarms(empty_pb2.Empty()):
    print(f" - ID={a.id}, Title={a.title}")

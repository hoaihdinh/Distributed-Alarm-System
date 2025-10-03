
# test for storage, scheduler, and notification node
# need to run node1.py, node2.py and node3.py and then this file

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

time.sleep(5)

# Schedule an alarm for 5 secs in the future
trigger_time = int(time.time()) + 5
alarm = alarm_pb2.Alarm(
    id=0,
    title="Wake up in 5 seconds",
    time={"seconds": trigger_time}  # timestamp in seconds
)
scheduler_stub.ScheduleAlarm(alarm)
print(f"Scheduled alarm for 5 sec in future: {trigger_time}")

# schedule alarm for 10 secs in future
trigger_time = int(time.time()) + 8
alarm = alarm_pb2.Alarm(
    id=0,
    title="Wake up in 8 seconds",
    time={"seconds": trigger_time}  
)
scheduler_stub.ScheduleAlarm(alarm)
print(f"Scheduled alarm for 8 sec in future: {trigger_time}")


# List alarms 
print("Listing alarms after:")
for a in storage_stub.ListAlarms(empty_pb2.Empty()):
    print(f" - ID={a.id}, Title={a.title}")

time.sleep(10)

# List alarms 
print("Listing alarms after both execute:")
for a in storage_stub.ListAlarms(empty_pb2.Empty()):
    print(f" - ID={a.id}, Title={a.title}")

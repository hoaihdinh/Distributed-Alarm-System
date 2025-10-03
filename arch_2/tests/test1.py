# tests storage node
# run node1.py before running this 

import grpc
from google.protobuf import empty_pb2
import alarm_pb2
import alarm_pb2_grpc

# Connect to server
channel = grpc.insecure_channel('localhost:50051')
stub = alarm_pb2_grpc.StorageStub(channel)

# Add alarm
alarm = alarm_pb2.Alarm(id=0, title="Test alarm")
stub.AddAlarm(alarm)
print("Added alarm")

# List alarms 
print("Listing alarms:")
for a in stub.ListAlarms(empty_pb2.Empty()):
    print(f" - ID={a.id}, Title={a.title}")

# Get alarm
resp = stub.GetAlarm(alarm_pb2.AlarmId(id=1))
print("Got alarm:", resp.title)

# Delete alarm with ID 1
stub.DeleteAlarm(alarm_pb2.AlarmId(id=1))
print("Deleted alarm:")
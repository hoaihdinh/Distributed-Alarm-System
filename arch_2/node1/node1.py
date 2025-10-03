## storage service/node server 
## will attempt to store alarms in local storage
## currently uses alarm_count to store IDs, not sure if we want to change
## can be run using python node1.py, test1.py calls all rpcs

import grpc
from concurrent import futures
from google.protobuf import empty_pb2

import alarm_pb2
import alarm_pb2_grpc

alarm_count = 1

class StorageServicer(alarm_pb2_grpc.StorageServicer):
    def __init__(self):
        # {id: alarm_pb2.Alarm}
        self.alarms = {}

    def AddAlarm(self, request, context):
        global alarm_count
        alarm = request
        if alarm.id == 0:
            alarm.id = alarm_count          # set new alarm ID to alarm_count
            alarm_count+=1
        self.alarms[alarm.id] = alarm       # store new alarm locally
        return empty_pb2.Empty()

    def GetAlarm(self, request, context):
        alarm_id = request.id
        alarm = self.alarms.get(alarm_id)
        if not alarm:
            return alarm_pb2.Alarm()  # alarm with alarm_id doesnt exist
        return alarm

    def ListAlarms(self, request, context):  # streams the current alarms
        for alarm in self.alarms.values():  
            yield alarm

    def DeleteAlarm(self, request, context):
        alarm_id = request.id
        if alarm_id in self.alarms:
            del self.alarms[alarm_id]
        return empty_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    alarm_pb2_grpc.add_StorageServicer_to_server(StorageServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Storage service listening on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
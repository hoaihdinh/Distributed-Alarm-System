## scheduler service node server


import grpc
from concurrent import futures
from google.protobuf import empty_pb2
import time
import asyncio


import alarm_pb2
import alarm_pb2_grpc

class SchedulerServicer(alarm_pb2_grpc.SchedulerServicer):
    def __init__(self, storage_stub=None):
        self.storage_channel = grpc.aio.insecure_channel("localhost:50051")  
        self.storage_stub = alarm_pb2_grpc.StorageStub(self.storage_channel)


    async def ScheduleAlarm(self, request, context):
        await self.storage_stub.AddAlarm(request)
        print(f"Scheduled alarm {request.id} for {request.time}")
        return empty_pb2.Empty()

    # sends due alarm to the notification service
    async def FwdDueAlarm(self, request, context):
        while True:
            response = self.storage_stub.ListAlarms(empty_pb2.Empty())
            async for alarm in response:
                now = int(time.time())
                if alarm.time.seconds <= now:
                    # deletes due alarm, later implement recurring logic
                    self.storage_stub.DeleteAlarm(alarm_pb2.AlarmId(id=alarm.id)) 
                    print(f"Alarm {alarm.id} is due")
                    return alarm
                

async def serve():
    server = grpc.aio.server()
    alarm_pb2_grpc.add_SchedulerServicer_to_server(SchedulerServicer(), server)
    server.add_insecure_port(f"[::]:50052")
    await server.start()
    print(f"Scheduler service listening on port 50052")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
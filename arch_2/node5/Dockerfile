# syntax=docker/dockerfile:1

FROM python:3.12

WORKDIR /app
COPY node5.py .
COPY alarm_pb2.py alarm_pb2_grpc.py .

RUN pip install --no-cache-dir grpcio grpcio-tools protobuf

CMD ["python", "node5.py"]

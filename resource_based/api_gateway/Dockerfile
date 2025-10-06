# syntax=docker/dockerfile:1

FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_gateway.py .

CMD ["uvicorn", "api_gateway:app", "--host", "0.0.0.0", "--port", "5000"]

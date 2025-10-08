# syntax=docker/dockerfile:1

FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py .
COPY src/models.py .
COPY src/schemas.py .
COPY src/database.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]

from event_scheduler import startup, schedule_alarm_event, delete_alarm_event, shutdown
from pydantic_models import EventTime
from fastapi import FastAPI

app = FastAPI(title="Event Scheduler")

@app.on_event("startup")
async def on_startup():
    await startup()

@app.on_event("shutdown")
async def on_shutdown():
    await shutdown()

@app.get("/")
def root():
    return {"message": "Event Scheduler is running"}

@app.api_route("/events/{alarm_id}", methods=["POST", "PUT"])
def add_event(alarm_id: int, event_time: EventTime):
    schedule_alarm_event(alarm_id, event_time.time)
    print(f"Scheduled alarm {alarm_id} for {event_time.time}")
    return {"message": f"Scheduled alarm {alarm_id} for {event_time.time}"}

@app.delete("/events/{alarm_id}")
def delete_event(alarm_id: int):
    delete_alarm_event(alarm_id)

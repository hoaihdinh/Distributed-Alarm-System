from fastapi import FastAPI, HTTPException, Request
from schemas import Alarm, UpdateAlarm
from models import AlarmDB
from database import SessionLocal, init_db
from event_scheduler import create_event, update_event, delete_event

app = FastAPI(title="Alarm Manager")

# Create tables
@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def root():
    return {"message": "Alarm Manager is running"}

@app.post("/alarms")
def create_alarm(alarm: Alarm):
    with SessionLocal() as db:
        new_alarm = AlarmDB(**alarm.dict())
        db.add(new_alarm)
        db.commit()
        db.refresh(new_alarm)

        create_event(alarm_id=new_alarm.id, time=new_alarm.time)

        return new_alarm

@app.get("/alarms/{alarm_id}")
def get_alarm(alarm_id: int):
    with SessionLocal() as db:
        alarm = db.query(AlarmDB).filter(AlarmDB.id == alarm_id).first()
        if not alarm:
            raise HTTPException(status_code=404, detail="Alarm not found")
        return alarm
    
@app.get("/alarms")
def get_user_alarms(user_id: int | None = None, status: str | None = None):
    with SessionLocal() as db:
        query = db.query(AlarmDB)

        if user_id:
            query = query.filter(AlarmDB.user_id == user_id)
        if status:
            query = query.filter(AlarmDB.status == status)
        
        return query.all()

@app.put("/alarms/{alarm_id}")
def update_alarm(alarm_id: int, updated_fields: UpdateAlarm):
    with SessionLocal() as db:
        alarm = db.query(AlarmDB).filter(AlarmDB.id == alarm_id).first()
        if not alarm:
            raise HTTPException(status_code=404, detail="Alarm not found")
        for key, value in updated_fields.dict(exclude_unset=True).items():
            setattr(alarm, key, value)
        db.commit()
        db.refresh(alarm)

        if updated_fields.time:
            update_event(alarm_id=alarm.id, time=alarm.time)

        return alarm

@app.delete("/alarms/{alarm_id}")
def delete_alarm(alarm_id: int):
    with SessionLocal() as db:
        alarm = db.query(AlarmDB).filter(AlarmDB.id == alarm_id).first()
        if not alarm:
            raise HTTPException(status_code=404, detail="Alarm not found")
        db.delete(alarm)
        db.commit()
        delete_event(alarm_id)
        return {"deleted_id": alarm_id}

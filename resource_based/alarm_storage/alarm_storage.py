from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
from datetime import datetime
from database_setup import AlarmDB, SessionLocal, init_db

app = FastAPI(title="Alarm Storage Service")

# Create tables on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Pydantic model
class Alarm(BaseModel):
    user_id: int
    message: str
    time: datetime

@app.get("/")
def root():
    return {"message": "Alarm Storage Service is running"}

@app.post("/alarms")
def create_alarm(alarm: Alarm):
    with SessionLocal() as db:
        new_alarm = AlarmDB(**alarm.dict())
        db.add(new_alarm)
        db.commit()
        db.refresh(new_alarm)
        return new_alarm

@app.get("/alarms/{alarm_id}")
def get_alarm(alarm_id: int):
    with SessionLocal() as db:
        alarm = db.query(AlarmDB).filter(AlarmDB.id == alarm_id).first()
        if not alarm:
            raise HTTPException(status_code=404, detail="Alarm not found")
        return alarm
    
@app.get("/alarms/user/{user_id}")
def get_user_alarms(user_id: int):
    with SessionLocal() as db:
        alarms = db.query(AlarmDB).filter(AlarmDB.user_id == user_id).all()
        if not alarms:
            raise HTTPException(status_code=404, detail=f"No alarms found for user {user_id}")
        return alarms

@app.put("/alarms/{alarm_id}")
def update_alarm(alarm_id: int, updated: Alarm):
    with SessionLocal() as db:
        alarm = db.query(AlarmDB).filter(AlarmDB.id == alarm_id).first()
        if not alarm:
            raise HTTPException(status_code=404, detail="Alarm not found")
        for key, value in updated.dict().items():
            setattr(alarm, key, value)
        db.commit()
        db.refresh(alarm)
        return alarm

@app.delete("/alarms/{alarm_id}")
def delete_alarm(alarm_id: int):
    with SessionLocal() as db:
        alarm = db.query(AlarmDB).filter(AlarmDB.id == alarm_id).first()
        if not alarm:
            raise HTTPException(status_code=404, detail="Alarm not found")
        db.delete(alarm)
        db.commit()
        return {"deleted_id": alarm_id}

from fastapi import FastAPI, HTTPException, Request
from resource_based.alarm_database.schemas import Alarm, UpdateAlarm
from resource_based.alarm_database.database import AlarmDB, SessionLocal, init_db

app = FastAPI(title="Alarm Database")

# Create tables
@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def root():
    return {"message": "Alarm Database is running"}

@app.post("/alarms")
def create_alarm(alarm: Alarm):
    with SessionLocal() as db:
        new_alarm = AlarmDB(**alarm.dict())
        db.add(new_alarm)
        db.commit()
        db.refresh(new_alarm)
        return new_alarm

@app.get("/alarms/{status}")
def get_alarms_with_status(status: str):
    with SessionLocal() as db:
        return db.query(AlarmDB).filter(AlarmDB.status == status).all()

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
def update_alarm(alarm_id: int, updated_fields: UpdateAlarm):
    with SessionLocal() as db:
        alarm = db.query(AlarmDB).filter(AlarmDB.id == alarm_id).first()
        if not alarm:
            raise HTTPException(status_code=404, detail="Alarm not found")
        for key, value in updated_fields.dict(exclude_unset=True).items():
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

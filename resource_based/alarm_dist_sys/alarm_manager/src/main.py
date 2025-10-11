from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import asc
from pydantic_models import Alarm, UpdateAlarm
from database_models import AlarmDB
from database import SessionLocal, init_db

app = FastAPI(title="Alarm Manager")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def root():
    return {"message": "Alarm Manager is running"}
    
@app.get("/alarms")
def get_all_alarms(user_id: int | None = None, status: str | None = None):
    with SessionLocal() as db:
        query = db.query(AlarmDB)

        if user_id:
            query = query.filter(AlarmDB.user_id == user_id)
        if status:
            query = query.filter(AlarmDB.status == status)
        
        return query.order_by(asc(AlarmDB.time)).all()

@app.get("/alarms/{alarm_id}")
def get_alarm(alarm_id: int):
    with SessionLocal() as db:
        alarm = db.query(AlarmDB).filter(AlarmDB.id == alarm_id).first()
        if not alarm:
            raise HTTPException(status_code=404, detail="Alarm not found")
        return alarm

@app.post("/alarms")
def create_alarm(alarm: Alarm):
    with SessionLocal() as db:
        new_alarm = AlarmDB(**alarm.dict())
        db.add(new_alarm)
        db.commit()
        db.refresh(new_alarm)
        print(f"[Alarm Manager] Added alarm: id={new_alarm.id}, time={new_alarm.time}, message={new_alarm.message}, status={new_alarm.status}")

        return new_alarm

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

        print(f"[Alarm Manager] Updated alarm alarm: id={alarm.id}, time={alarm.time}, message={alarm.message}, status={alarm.status}")
        return alarm

@app.delete("/alarms")
def delete_alarms_under_user(user_id: int = Query(...)):
    with SessionLocal() as db:
        # Bulk delete all alarms corresponding to the user
        deleted_count = db.query(AlarmDB).filter(AlarmDB.user_id == user_id).delete(synchronize_session=False)
        db.commit()

        print(f"[Alarm Manager] Deleted alarms under {user_id}")
        return {"deleted": deleted_count}

@app.delete("/alarms/{alarm_id}")
def delete_alarm(alarm_id: int):
    with SessionLocal() as db:
        alarm = db.query(AlarmDB).filter(AlarmDB.id == alarm_id).first()
        if not alarm:
            raise HTTPException(status_code=404, detail="Alarm not found")
        db.delete(alarm)
        db.commit()

        print(f"[Alarm Manager] Deleted alarm: id={alarm.id}, time={alarm.time}, message={alarm.message}, status={alarm.status}")
        return {"deleted_id": alarm_id}

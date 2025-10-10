from fastapi import FastAPI, HTTPException, Query
from pydantic_models import Alarm, UpdateAlarm
from database_models import AlarmDB
from database import SessionLocal, init_db
from event_scheduler import create_event, update_event, delete_event

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
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        
        return query.all()

@app.get("/alarms/{alarm_id}")
def get_alarm(alarm_id: int):
    with SessionLocal() as db:
        alarm = db.query(AlarmDB).filter_by(id=alarm_id).first()
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
        print(f"[Alarm Manager] Added alarm: id={new_alarm.id}, time={new_alarm.time}, message={new_alarm.message}")
        create_event(alarm_id=new_alarm.id, time=new_alarm.time)

        return new_alarm

@app.put("/alarms/{alarm_id}")
def update_alarm(alarm_id: int, updated_fields: UpdateAlarm):
    with SessionLocal() as db:
        alarm = db.query(AlarmDB).filter_by(id=alarm_id).first()
        if not alarm:
            raise HTTPException(status_code=404, detail="Alarm not found")
        for key, value in updated_fields.dict(exclude_unset=True).items():
            setattr(alarm, key, value)
        db.commit()
        db.refresh(alarm)

        if updated_fields.time:
            update_event(alarm_id=alarm.id, time=alarm.time)

        print(f"[Alarm Manager] Added alarm: id={alarm.id}, time={alarm.time}, message={alarm.message}")
        return alarm

@app.delete("/alarms")
def delete_alarms_under_user(user_id: int = Query(...)):
    with SessionLocal() as db:
        # Fetches alarms that are pending under user, and deletes those corresponding events from the scheduler
        alarm_ids = db.query(AlarmDB.id).filter_by(user_id=user_id, status="pending").scalars().all()
        for alarm_id in alarm_ids:
            delete_event(alarm_id)

        # Bulk delete all alarms corresponding to the user
        deleted_count = db.query(AlarmDB).filter_by(user_id=user_id).delete(synchronize_session=False)
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
        print(f"[Alarm Manager] Added alarm: id={alarm.id}, time={alarm.time}, message={alarm.message}")
        delete_event(alarm_id)
        return {"deleted_id": alarm_id}

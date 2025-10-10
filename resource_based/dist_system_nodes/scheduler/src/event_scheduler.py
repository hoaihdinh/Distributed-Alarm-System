from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
import aiohttp
import requests

ALARM_URL = "http://alarm_manager:5001/alarms"
NOTIFY_URL = "http://notification_manager:5004/notify"

scheduler = AsyncIOScheduler()
session: aiohttp.ClientSession | None = None

async def create_notification(alarm_id: int):
    try:
        # Updates the alarm status to notified
        async with session.put(
            f"{ALARM_URL}/{alarm_id}",
            json={"status": "notified"},
        ) as response:
            if response.status == 200:
                alarm = await response.json()
                print(f"[Scheduler] Alarm {alarm_id} updated status to notified")
            else:
                print(f"[Scheduler] Failed to update alarm {alarm_id}: {response.status}")

        # Notifies the corresponding user about the alarm
        async with session.post(
            f"{NOTIFY_URL}/{alarm["user_id"]}",
            json={"message": alarm["message"]}
        ) as notify_response:
            print(f"[Scheduler] Alarm {alarm_id} POST to notification_manager")

        print(f"[Scheduler] Alarm {alarm_id} executed and removed event")
    except Exception as e:
        print(f"[Scheduler] Alarm {alarm_id} error while executing event: {e}")

def schedule_alarm_event(alarm_id: int, time: datetime) -> dict[str, str]:
    # If job with same ID exists, remove it first
    existing = scheduler.get_job(str(alarm_id))
    if existing:
        scheduler.remove_job(str(alarm_id))

    trigger = DateTrigger(run_date=time)
    scheduler.add_job(
        create_notification,
        trigger=trigger,
        id=str(alarm_id),
        args=[alarm_id],
        misfire_grace_time=60,  # run up to 60s late if missed
        coalesce=True
    )

    print(f"[Scheduler] Scheduled alarm {alarm_id} at {time.isoformat()} UTC")

    # Ensures both times are in the same timezone (UTC), enables subtraction
    now = datetime.now(timezone.utc)
    if time.tzinfo is None:
        time = time.replace(tzinfo=timezone.utc)

    # Handles overdue alarms
    if (now - time).total_seconds() > 60:
        response = requests.put(f"{ALARM_URL}/{alarm_id}", json={"status": "late"})
        alarm = response.json()
        requests.post(f"{NOTIFY_URL}/{alarm["user_id"]}", json={"message": alarm["message"]})
        
        print(f"[Scheduler] Alarm {alarm_id} executed overdue event")
        
        return {"message": f"Notification for Alarm {alarm_id} sent, alarm is overdue."}

    return {"message": f"Scheduled Alarm {alarm_id} successfully."}

def delete_alarm_event(alarm_id: int) -> bool:
    job = scheduler.get_job(str(alarm_id))
    if job:
        scheduler.remove_job(str(alarm_id))
        print(f"[Scheduler] Alarm {alarm_id} cancelled")
        return True
    
    return False

async def schedule_all_pending_alarms():
    async with session.get(f"{ALARM_URL}", params={"status": "pending"}) as response:
        if response.status != 200:
            print(f"[Scheduler] Failed to fetch pending alarms ({response.status})")
            return

        alarms = await response.json()
        print(f"[Scheduler] Retrieved {len(alarms)} pending alarms")

        for alarm in alarms:
            try:
                time = datetime.fromisoformat(alarm["time"])
                schedule_alarm_event(alarm["id"], time)
            except Exception as e:
                print(f"[Scheduler] Error scheduling alarm {alarm['id']}: {e}")

async def startup():
    global session
    session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5))
    scheduler.start()
    await schedule_all_pending_alarms()

async def shutdown():
    scheduler.shutdown(wait=False)
    await session.close()

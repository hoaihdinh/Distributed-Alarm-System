from datetime import datetime
import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

ALARM_URL = "http://alarm_manager:5001/alarms"
NOTIFY_URL = "http://notification_manager:5004/notify"

scheduler = AsyncIOScheduler()
session: aiohttp.ClientSession | None = None

async def create_notification(alarm_id: int, scheduled_time: datetime):
    try:
        async with session.get(f"{ALARM_URL}/{alarm_id}") as response:
            if response.status != 200:
                print(f"[Alarm {alarm_id}] fetch failed ({response.status})")
                return
            alarm = dict(await response.json())

        # Verify that alarm data is consistent (has not been notified and time is the same)
        if alarm["status"] == "pending" and datetime.fromisoformat(alarm["time"]) == scheduled_time:
            async with session.put(
                f"{ALARM_URL}/{alarm_id}",
                json={"status": "ready"},
            ) as put_response:
                print(f"[Alarm {alarm_id}] ready → {put_response.status}")

            async with session.post(
                f"{NOTIFY_URL}/{alarm["user_id"]}",
                json={"message": alarm["message"]}
            ) as notify_response:
                print(f"POST notify request")
    
        print(f"Removing event with [Alarm {alarm_id}]")
        scheduler.remove_job(str(alarm_id)) # remove the event as the job has been triggered

    except Exception as e:
        print(f"[Alarm {alarm_id}] error: {e}")

def schedule_alarm_event(alarm_id: int, time: datetime):
    # If job with same ID exists, remove it first
    existing = scheduler.get_job(str(alarm_id))
    if existing:
        scheduler.remove_job(str(alarm_id))

    trigger = DateTrigger(run_date=time)
    scheduler.add_job(
        create_notification,
        trigger=trigger,
        id=str(alarm_id),
        args=[alarm_id, time],
        misfire_grace_time=60,  # run up to 60s late if missed
        coalesce=True
    )

    print(f"[Scheduler] Scheduled alarm {alarm_id} at {time.isoformat()}")

def delete_alarm_event(alarm_id: int):
    job = scheduler.get_job(str(alarm_id))
    if job:
        scheduler.remove_job(str(alarm_id))
        print(f"[Scheduler] Cancelled alarm {alarm_id}")

async def startup():
    global session
    session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5))
    scheduler.start()
    print("[Scheduler] Started")

async def shutdown():
    scheduler.shutdown(wait=False)
    await session.close()
    print("[Scheduler] Stopped")

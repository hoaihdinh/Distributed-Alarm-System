from fastapi import FastAPI, Request, Query
from fastapi.responses import StreamingResponse
from pydantic_models import Message
from database_models import NotificationDB
from database import SessionLocal, init_db
import asyncio
from typing import Dict
import json

app = FastAPI(title="Notification Manager")

# Keep a queue of messages per user
user_queues: Dict[int, asyncio.Queue] = {}

@app.on_event("startup")
async def startup_event():
    init_db()

    # Load undelivered notifications into queues
    with SessionLocal() as db:
        undelivered = db.query(NotificationDB).filter_by(delivered=False).all()
        for notif in undelivered:
            if notif.user_id not in user_queues:
                user_queues[notif.user_id] = asyncio.Queue()
            await user_queues[notif.user_id].put({"id": notif.id, "message": notif.message})
            print(f"[Notification Manager] Added notification \"{notif.message}\" to queue for User {notif.user_id}")

@app.get("/")
def root():
    return {"message": "Notification Manager running"}

# SSE stream endpoint
@app.get("/notifications/stream")
async def notifications_stream(user_id: int = Query(...)):
    if user_id not in user_queues:
        user_queues[user_id] = asyncio.Queue()

    async def event_generator(queue: asyncio.Queue):
        try:
            while True:
                message = await queue.get()  # wait for new messages

                # Mark as delivered in the database
                notif_id = message.get("id")
                if notif_id:
                    with SessionLocal() as db:
                        notif = db.query(NotificationDB).get(notif_id)
                        if notif:
                            notif.delivered = True
                            db.commit()

                print(f"[Notification Manager] Pushing notification \"{json.dumps(message)}\" to User {user_id}")
                yield f"data: {json.dumps(message)}\n\n" # Sends it via SSE
        except asyncio.CancelledError:
            pass

    return StreamingResponse(event_generator(user_queues[user_id]), media_type="text/event-stream")

@app.post("/notify/{user_id}")
async def notify_user(user_id: int, msg: Message):
    if user_id not in user_queues:
        user_queues[user_id] = asyncio.Queue()

    # Add the notification to the database
    with SessionLocal() as db:
        new_notif = NotificationDB(user_id=user_id, message=msg.message)
        db.add(new_notif)
        db.commit()
        db.refresh(new_notif)

    # Add the notification to the queue
    await user_queues[user_id].put({"id": new_notif.id, "message": msg.message})
    
    print(f"[Notification Manager] Added notification \"{msg.message}\" to queue for User {user_id}")
    return {"status": "queued"}

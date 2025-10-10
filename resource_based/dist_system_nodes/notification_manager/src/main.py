from fastapi import FastAPI, Request, Query
from fastapi.responses import StreamingResponse
from pydantic_models import Message
import asyncio
from typing import Dict
import json

app = FastAPI(title="Notification Manager")

# Keep a queue of messages per user
user_queues: Dict[int, asyncio.Queue] = {}

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
                yield f"data: {json.dumps(message)}\n\n"
        except asyncio.CancelledError:
            pass

    return StreamingResponse(event_generator(user_queues[user_id]), media_type="text/event-stream")

@app.post("/notify/{user_id}")
async def notify_user(user_id: int, msg: Message):
    if user_id not in user_queues:
        user_queues[user_id] = asyncio.Queue()
    await user_queues[user_id].put({"message": msg.message})
    return {"status": "queued"}

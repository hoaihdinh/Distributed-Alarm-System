from datetime import datetime
from pydantic import BaseModel

class EventTime(BaseModel):
    time: datetime
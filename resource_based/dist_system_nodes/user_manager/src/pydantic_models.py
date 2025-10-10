from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

class UpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

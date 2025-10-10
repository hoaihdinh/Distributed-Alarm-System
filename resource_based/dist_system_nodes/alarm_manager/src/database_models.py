from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class AlarmDB(Base):
    __tablename__ = "alarms"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False, default="pending")
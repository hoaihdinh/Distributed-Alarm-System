from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://alarmuser:alarmpass@postgres:5432/alarmdb"

engine = create_engine(
    DATABASE_URL,
    pool_size=20,         # more concurrent connections
    max_overflow=40,      # allow temporary spikes
    pool_timeout=30,      # seconds to wait for a connection
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

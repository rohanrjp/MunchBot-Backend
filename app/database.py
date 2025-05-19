from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from .config import settings
import time

POOL_SIZE = 5  
MAX_OVERFLOW = 10  
POOL_TIMEOUT = 30  
POOL_RECYCLE = 1800  

engine = create_engine(
    settings.DB_STRING,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=POOL_TIMEOUT,
    pool_recycle=POOL_RECYCLE,
    pool_pre_ping=True  
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def init_db(retries: int = 5, delay: int = 3):
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            print("Database connection established.")
            return
        except OperationalError as e:
            print(f"DB connection failed (attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                print(f"⏳ Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Could not connect to the database after several attempts.")
                raise
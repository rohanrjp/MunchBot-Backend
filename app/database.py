from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

engine=create_engine(url=settings.DB_STRING,pool_size=20,max_overflow=0,pool_timeout=30,pool_recycle=3600)
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base=declarative_base()

def init_db():
    print("Tables in DB created")
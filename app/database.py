from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

engine=create_engine(url=settings.DB_STRING,pool_pre_ping=True,pool_size=10,max_overflow=5,pool_recycle=1800)
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base=declarative_base()

def init_db():
    print("Tables in DB created")
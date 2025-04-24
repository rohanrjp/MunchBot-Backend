from sqlalchemy import Column,String,DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from ..database import Base
import uuid
from zoneinfo import ZoneInfo
from datetime import datetime

IST=ZoneInfo("Asia/Kolkata")

class User(Base):
    
    __tablename__="user_details"
    
    uuid=Column(PG_UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    hashed_password=Column(String,nullable=False)
    joining_date=Column(DateTime,nullable=False,default=lambda : datetime.now(IST))
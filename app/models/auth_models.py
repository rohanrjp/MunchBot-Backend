from sqlalchemy import Column,String,DateTime,Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from ..database import Base
import uuid
from sqlalchemy.orm import relationship

class User(Base):
    
    __tablename__="user_details"
    
    uuid=Column(PG_UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    hashed_password=Column(String,nullable=False)
    joining_date=Column(DateTime,nullable=False)
    is_pro=Column(Boolean,nullable=False)
    
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("UserGoal", back_populates="user", uselist=False, cascade="all, delete-orphan") 
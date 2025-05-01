import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base
from sqlalchemy.orm import relationship


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_details.uuid", ondelete="CASCADE"), nullable=False)
    chat_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    sender = Column(String, nullable=False)  
    message = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True))
    chat_date = Column(String, nullable=False)
    
    user = relationship("User", back_populates="chat_messages")
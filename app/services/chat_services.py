from datetime import date,datetime
from uuid import uuid4,UUID
from sqlalchemy.orm import Session
from ..models.chat_model import ChatMessage
from sqlalchemy import cast,Date

def store_chat_message(db: Session, user_id:UUID,message:str, sender:str,message_timestamp:datetime,message_date:date)->None:
    
    chat_message = ChatMessage(
        user_id=user_id,
        chat_id=uuid4(),
        message=message,
        sender=sender,
        timestamp=message_timestamp,
        chat_date=message_date
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    
def retrieve_chat_messages(db:Session,user_id: UUID,date:date):
    
    messages= db.query(ChatMessage).filter(
        user_id==ChatMessage.user_id,
        cast(ChatMessage.chat_date, Date) == date
    ).order_by(
        ChatMessage.timestamp.asc()
    ).all()
    
    return [
        {"id":m.id,"sender": m.sender, "message": m.message, "timestamp": m.timestamp}
        for m in messages
    ]
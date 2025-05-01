from datetime import date, timezone,datetime
from uuid import uuid4,UUID
from sqlalchemy.orm import Session
from ..models.chat_model import ChatMessage
from ..utils import convert_utc_to_ist
from sqlalchemy import cast,Date

current_utc_datetime=datetime.now(timezone.utc)
current_ist_datetime=convert_utc_to_ist(current_utc_datetime)

def store_chat_message(db: Session, user_id:UUID,message:str, sender:str)->None:
    
    chat_message = ChatMessage(
        user_id=user_id,
        chat_id=uuid4(),
        message=message,
        sender=sender,
        timestamp=current_ist_datetime,
        chat_date=current_ist_datetime.date().isoformat()
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
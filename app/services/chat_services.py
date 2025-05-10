from datetime import date,datetime
from uuid import uuid4,UUID
from sqlalchemy.orm import Session
from ..models.chat_model import ChatMessage
from sqlalchemy import cast,Date
from app.agents.nutri_summary_agent import nutrition_summary_agent
from app.models.nutrition_summary_model import DailyNutritionSummary

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
 
def retrieve_bot_messages(db: Session,user_id: UUID,selected_date:date):
    
    messages=db.query(ChatMessage).filter(
        user_id==ChatMessage.user_id,
        cast(ChatMessage.chat_date, Date) == selected_date,
        ChatMessage.sender=="assistant"
    ).order_by(
        ChatMessage.timestamp.asc()
    ).all()
    
    return messages
         
async def summarise_daily_nutrition_messages(db: Session,user_id: UUID,selected_date: date)->None:
    bot_messages=retrieve_bot_messages(db,user_id,selected_date)    
    
    if not bot_messages:
        return None
    else:
        input_to_agent= "/n".join([msg.message for msg in bot_messages])
        output= await nutrition_summary_agent.run(input_to_agent)
        
    try:
        summary = db.query(DailyNutritionSummary).filter_by(
            user_id=user_id,
            date=selected_date
        ).first()

        if summary:
            summary.calories = output.output.calories
            summary.protein = output.output.protein
            summary.carbs = output.output.carbs
            summary.sugar = output.output.sugar
            summary.fats = output.output.fats
        else:
            summary = DailyNutritionSummary(
                user_id=user_id,
                date=selected_date,
                calories=output.output.calories,
                protein=output.output.protein,
                carbs=output.output.carbs,
                sugar=output.output.sugar,
                fats=output.output.fats
            )
            db.add(summary)

        db.commit()
        db.refresh(summary)
        return summary

    except Exception as e:
        db.rollback()
        raise e
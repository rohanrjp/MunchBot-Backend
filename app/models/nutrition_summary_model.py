from sqlalchemy import Column, Date, Float, ForeignKey,func,DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base 

class DailyNutritionSummary(Base):
    __tablename__ = "daily_nutrition_summary"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_details.uuid"), nullable=False)
    date = Column(Date, nullable=False)
    calories = Column(Float, nullable=False, default=0.0)
    protein = Column(Float, nullable=False, default=0.0)
    carbs = Column(Float, nullable=False, default=0.0)
    sugar = Column(Float, nullable=False, default=0.0)
    fats = Column(Float, nullable=False, default=0.0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
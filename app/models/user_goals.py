import uuid
from sqlalchemy import Column, ForeignKey, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base  
from sqlalchemy.orm import relationship

class UserGoal(Base):
    
    __tablename__ = "user_goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_details.uuid", ondelete="CASCADE"), nullable=False)

    calorie_goal = Column(Float, nullable=True)
    protein_goal = Column(Float, nullable=True)
    sugar_goal = Column(Float, nullable=True)
    fat_goal = Column(Float, nullable=True)
    carbs_goal = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    user = relationship("User", back_populates="goals")

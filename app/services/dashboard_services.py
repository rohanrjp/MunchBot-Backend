from sqlalchemy.orm import Session
from app.models.auth_models import User
from app.models.user_goals import UserGoal
from fastapi import HTTPException,status
from app.schemas.dashboard_schemas import UserGoalsUpdate


def update_user_goals(db:Session,user:User,user_goals_input:UserGoalsUpdate):
    
    user_goals = db.query(UserGoal).filter(
        UserGoal.user_id==user.uuid,
    ).first()
    
    if not user_goals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User goals not found")
    else:
        user_goals.calorie_goal=user_goals_input.calorie_goal
        user_goals.protein_goal=user_goals_input.protein_goal
        user_goals.carbs_goal=user_goals_input.carb_goal
        user_goals.fat_goal=user_goals_input.fats_goal
        user_goals.sugar_goal=user_goals_input.sugars_goal
        
    
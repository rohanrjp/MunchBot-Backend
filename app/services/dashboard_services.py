from datetime import date, timedelta
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.models.auth_models import User
from app.models.nutrition_summary_model import DailyNutritionSummary
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
        user_goals.calorie_goal=float(user_goals_input.targetCalories)
        user_goals.protein_goal=float(user_goals_input.targetProtein)
        user_goals.carbs_goal=float(user_goals_input.targetCarbs)
        user_goals.fat_goal=float(user_goals_input.targetFats)
        user_goals.sugar_goal=float(user_goals_input.targetSugars)
        db.commit()
        db.refresh(user_goals)
        
def retrieve_todays_intake_data(db: Session,user: User,todays_date:date):
    
    user_goals=db.query(UserGoal).filter(
        user.uuid==UserGoal.user_id
    ).first()
    
    if not user_goals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User goals not entered")
    
    calorie_goal=user_goals.calorie_goal
    protein_goal=user_goals.protein_goal
    sugar_goal=user_goals.sugar_goal
    carbs_goal=user_goals.carbs_goal
    fats_goal=user_goals.fat_goal
    
    todays_nutrition_summary=db.query(DailyNutritionSummary).filter(
        DailyNutritionSummary.user_id==user.uuid,
        DailyNutritionSummary.date==todays_date
    ).first()
    
    
    calories = todays_nutrition_summary.calories if todays_nutrition_summary else 0
    protein = todays_nutrition_summary.protein if todays_nutrition_summary else 0
    carbs = todays_nutrition_summary.carbs if todays_nutrition_summary else 0
    fats = todays_nutrition_summary.fats if todays_nutrition_summary else 0
    sugar = todays_nutrition_summary.sugar if todays_nutrition_summary else 0

    todays_intake_output_data={
            "calories": {
            "current": calories,
            "goal": calorie_goal,
            "unit": "kcal"
            },
            "protein": {
            "current": protein,
            "goal": protein_goal,
            "unit": "g"
            },
            "carbs": {
            "current": carbs,
            "goal": carbs_goal,
            "unit": "g"
            },
            "fats": {
            "current": fats,
            "goal": fats_goal,
            "unit": "g"
            },
            "sugar": { 
            "current": sugar,
            "goal": sugar_goal,
            "unit": "g"
            }
        }
    
    return todays_intake_output_data
    
 
def retrieve_weekly_intake_data(db: Session,user:User,todays_date:date):
    start_date = todays_date - timedelta(days=6)

    rows = db.query(DailyNutritionSummary).filter(
        DailyNutritionSummary.user_id == user.uuid,
        DailyNutritionSummary.date.between(start_date, todays_date)
    ).all()

    data_by_date = {row.date: row for row in rows}

    result = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        row = data_by_date.get(day)

        result.append({
            "date": day.strftime("%b %d"),  
            "calories": row.calories if row else 0,
            "proteins": row.protein if row else 0,
            "carbs": row.carbs if row else 0,
            "fats": row.fats if row else 0,
            "fullDate": day.isoformat()   
        })

    return jsonable_encoder(result)
    
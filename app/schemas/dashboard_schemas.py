from pydantic import BaseModel

class UserGoalsUpdate(BaseModel):
    calorie_goal:float
    protein_goal:float
    carb_goal:float
    fats_goal:float
    sugars_goal:float
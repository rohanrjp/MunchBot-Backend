from pydantic import BaseModel

class UserGoalsUpdate(BaseModel):
    targetCalories:float
    targetProtein:float
    targetSugars:float
    targetCarbs:float
    targetFats:float
    
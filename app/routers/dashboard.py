from fastapi import APIRouter,status
from fastapi.responses import JSONResponse
from ..dependancies.auth_dependancies import user_dependancy
from app.dependancies.db_dependencies import db_dependancy
from app.services.dashboard_services import update_user_goals
from app.schemas.dashboard_schemas import UserGoalsUpdate

dashboard_router=APIRouter(prefix='/dashboard',tags=['Dashboard'])

@dashboard_router.get('/me')
async def get_profile_details(user:user_dependancy):
    content={
        "name":user.name,
        "email":user.email, 
    }
    return JSONResponse(content=content,status_code=status.HTTP_200_OK)

@dashboard_router.post('/user_goals')
async def update_user_goals_rooute(db:db_dependancy,user:user_dependancy,user_goals:UserGoalsUpdate):
    update_user_goals(db,user,user_goals)
    content={
        'message':'User goals updated'
    }
    
    return JSONResponse(content=content,status_code=status.HTTP_202_ACCEPTED)
    
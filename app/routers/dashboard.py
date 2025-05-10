from datetime import date
from fastapi import APIRouter,status
from fastapi.responses import JSONResponse
from ..dependancies.auth_dependancies import user_dependancy
from app.dependancies.db_dependencies import db_dependancy
from app.services.dashboard_services import update_user_goals,retrieve_todays_intake_data,retrieve_weekly_intake_data
from app.schemas.dashboard_schemas import UserGoalsUpdate

dashboard_router=APIRouter(prefix='/dashboard',tags=['Dashboard'])

@dashboard_router.get('/me')
async def get_profile_details(user:user_dependancy):
    content={
        "name":user.name,
        "email":user.email, 
    }
    return JSONResponse(content=content,status_code=status.HTTP_200_OK)

@dashboard_router.get('/account/me')
async def get_profile_details(user:user_dependancy):
    plan_str="Pro Plan" if user.is_pro else "Free Plan"
    join_date = user.joining_date.strftime("%B %Y")
    content={
        "name":user.name,
        "email":user.email, 
        "plan":plan_str,
        "join_date":join_date
    }
    return JSONResponse(content=content,status_code=status.HTTP_200_OK)

@dashboard_router.post('/user_goals')
async def update_user_goals_rooute(db:db_dependancy,user:user_dependancy,user_goals:UserGoalsUpdate):
    update_user_goals(db,user,user_goals)
    content={
        'message':'User goals updated'
    }
    return JSONResponse(content=content,status_code=status.HTTP_202_ACCEPTED)

@dashboard_router.get('/dashboard_data/{todays_date}')
async def get_all_dashboard_data(db:db_dependancy,user:user_dependancy,todays_date:date):
    
    todays_intake_data=retrieve_todays_intake_data(db,user,todays_date)
    
    weekly_intake_data =retrieve_weekly_intake_data(db,user,todays_date)
    
    dashboard_data={
        'todays_intake':todays_intake_data,
        'weekly_intake':weekly_intake_data
    }
    
    return JSONResponse(content=dashboard_data,status_code=status.HTTP_200_OK)
    
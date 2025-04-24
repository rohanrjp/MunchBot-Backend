from fastapi import FastAPI
from .database import init_db
from .routers.auth import auth_router

app=FastAPI(title="Calorie GPT Tracker")

init_db()

app.include_router(auth_router)


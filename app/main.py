from fastapi import FastAPI
from .database import init_db
from .routers.auth import auth_router
from .routers.chat import chat_router
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="Calorie GPT Tracker")

init_db()

app.include_router(auth_router)
app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
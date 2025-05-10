from fastapi import FastAPI,status
from .database import init_db
from .routers.auth import auth_router
from .routers.chat import chat_router
from .routers.dashboard import dashboard_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .config import settings

def create_app()->FastAPI:
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("App started")
        init_db()
        yield 
        print("App stopped")     
        
    app=FastAPI(title="Munchbot",description="Calorie tracking assistant",lifespan=lifespan)
    
    app.include_router(auth_router)
    app.include_router(chat_router)
    app.include_router(dashboard_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
        
    return app
           
app=create_app()

@app.get('/health-check',status_code=status.HTTP_200_OK,tags=["Health Check"])
async def ping():
    return {"message":"Server running"}  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.GCLOUD_PORT)   

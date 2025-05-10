from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DB_STRING:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    SECRET_KEY:str
    GEMINI_API_KEY:str
    REDIS_CLOUD_PASSWORD:str
    REDIS_CLOUD_HOST:str
    REDIS_CLOUD_PORT:int
    REDIS_CLOUD_USERNAME:str
    ALEMBIC_CONNECTION:str
    GCLOUD_PORT:int
        
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
settings=Settings()    


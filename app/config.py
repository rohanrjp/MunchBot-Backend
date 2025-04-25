from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DB_STRING:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    SECRET_KEY:str
    GEMINI_API_KEY:str
    
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
settings=Settings()    


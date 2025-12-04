"""
Configuration management.
TODO: You'll implement this step by step.
"""
# This file will be built step by step
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_NAME: str = "academic_search"
    DB_USER: str  = "postgres"
    DB_PASSWORD: str  = ""
    DB_HOST: str   = "localhost"
    DB_PORT: int   = 5432
     
    class Config:
        env_file = ".env"

    
settings = Settings()

def get_database_url() -> str:
    '''Postgres databse url connection'''
    return f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
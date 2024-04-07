from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
    """
        Configurações gerais usadas na aplicação
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = f'sqlite+aiosqlite:////home/dgamorim/development/recomendation_poc/database/recommendation.db?charset=utf8'
    DBBaseModel: ClassVar = declarative_base()
    
    class Config:
        case_sensitive = True
        
settings = Settings()
from sqlalchemy import Column, Integer, String, JSON
from core.configs import settings

class RecommendationModel(settings.DBBaseModel):
    __tablename__ = 'recommendation'
    
    id:int = Column(Integer, primary_key=True, autoincrement=True)
    members:str = Column(String)
    vouchers_recommendation:list[str] = Column(String)
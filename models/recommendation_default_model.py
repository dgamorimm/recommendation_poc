from sqlalchemy import Column, Integer, String
from core.configs import settings

class RecommendationDefaultModel(settings.DBBaseModel):
    __tablename__ = 'recommendation_default'
    
    id:int = Column(Integer, primary_key=True, autoincrement=True)
    shoppings:str = Column(String)
    vouchers_recommendation:list[str] = Column(String)
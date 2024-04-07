
from pydantic import BaseModel as SCBaseModel
from typing import List
import json

class RecommendationSchema(SCBaseModel):
    # id: int
    # members: str
    vouchers_recommendation: List
    
    class Config:
        from_attributes = True
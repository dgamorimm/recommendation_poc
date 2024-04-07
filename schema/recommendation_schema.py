
from pydantic import BaseModel as SCBaseModel
from typing import List, Optional

class RecommendationSchema(SCBaseModel):
    vouchers_recommendation: Optional[List] = None
    vouchers_recommendation_default: Optional[List] = None
    
    class Config:
        from_attributes = True
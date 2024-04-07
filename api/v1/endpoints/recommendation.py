from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

from models.recommendation_model import RecommendationModel
from schema.recommendation_schema import RecommendationSchema
from core.deps import get_session
import json

router = APIRouter()

@router.get('/{member_id}', response_model=RecommendationSchema,status_code=status.HTTP_200_OK)
async def get_curso(member_id:str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RecommendationModel).where(RecommendationModel.members == member_id)
    
        # query = text(f"""SELECT recommendation.id, recommendation.members, recommendation.vouchers_recommendation FROM recommendation WHERE recommendation.members = '{member_id}'""")

        try:
            result = await session.execute(query)
            member = result.scalars().first()
        except:
            member = None

        if member:
            return {"vouchers_recommendation": json.loads(member.vouchers_recommendation)}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Erro ao buscar os vouchers do membro de ID:{member_id}')
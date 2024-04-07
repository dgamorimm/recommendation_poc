from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

from models.recommendation_model import RecommendationModel
from models.recommendation_default_model import RecommendationDefaultModel
from schema.recommendation_schema import RecommendationSchema
from core.deps import get_session
import json
import polars as pl

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
            member = []
        
        df_voucher = pl.read_parquet('datasets/input/base_voucher.parquet')
        df_member_default = df_voucher.filter(pl.col('member_id') == member_id)
        try:
            shopping =  df_member_default['shopping'].unique().to_list()[0]
            query = select(RecommendationDefaultModel).where(RecommendationDefaultModel.shoppings == shopping)
            result = await session.execute(query)
            member_default = result.scalars().first()
        except:
            member_default = []

        member = json.loads(member.vouchers_recommendation) if member else []
        member_default = json.loads(member_default.vouchers_recommendation) if member_default else []
        if (len(member) > 0) | (len(member_default) > 0):
            return {"vouchers_recommendation": member, "vouchers_recommendation_default": member_default}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Erro ao buscar os vouchers do membro de ID:{member_id}')
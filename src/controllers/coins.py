from typing import List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.core.containers import Container
from src.services.conigecko.api import CoingeckoApiService

router = APIRouter()


class CoinSchema(BaseModel):
    id: str
    symbol: str
    name: str


class CoinListResponseSchema(BaseModel):
    status: int
    coins: List[CoinSchema]


@router.get("/v1/coins", response_model=CoinListResponseSchema, response_model_exclude_unset=True)
@inject
async def get_coins_trends(
    coingecko_service: CoingeckoApiService = Depends(Provide[Container.coingecko_service]),
):
    return await coingecko_service.get_coin_list()

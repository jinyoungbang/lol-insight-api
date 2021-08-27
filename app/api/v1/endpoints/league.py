from fastapi import APIRouter
from app.api.v1.middlewares.league_client import get_user_puuid

router = APIRouter()


@router.get("/test")
async def test_router():
    """ Get real-time price for the selected cryptocurrency in the currency of your choice"""
    return {"test": "test"}


@router.get("/find-insights/{game_name}")
async def find_insights(game_name):
    user_puuid = get_user_puuid(game_name, "NA1")
    match_history_id
    return user_puuid

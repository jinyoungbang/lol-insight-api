from fastapi import APIRouter
from app.api.v1.middlewares.league_client import get_user_puuid, get_match_history_id, get_insights_from_match, get_user_insights_from_match
from app.api.v1.middlewares.league_stats import return_match_insight

router = APIRouter()


@router.get("/test")
async def test_router():
    """ Get real-time price for the selected cryptocurrency in the currency of your choice"""
    return {"test": "test"}


@router.get("/find-insights/{region}/{game_name}")
async def find_insights(region: str, game_name: str):
    user_puuid = get_user_puuid(game_name, region)
    match_history_id = get_match_history_id(user_puuid)
    for match_id in match_history_id:
        match_insight = get_user_insights_from_match(match_id, user_puuid)
        match_insight = return_match_insight(match_insight)
        return match_insight
    return match_history_id

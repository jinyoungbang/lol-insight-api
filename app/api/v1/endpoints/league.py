from fastapi import APIRouter
from app.api.v1.middlewares.league_client import UserInfo
from app.api.v1.middlewares.league_stats import return_match_insight

router = APIRouter()


@router.get("/test")
async def test_router():
    """ Get real-time price for the selected cryptocurrency in the currency of your choice"""
    return {"test": "test"}


@router.get("/find-insights/{region}/{game_name}")
async def find_insights(region: str, game_name: str):
    try:
        user_info = UserInfo(region, game_name)
        user_info.set_region_router()
        user_info.set_puuid()
        if not user_info.is_valid_user:
            return {
                "status": False,
                "message": f"User with the name, {user_info.game_name} does not exist."
            }
        user_info.get_match_history_id()
        if len(user_info.match_history_ids) == 0:
            return {
                "status": False,
                "message": "No matches found."
            }
        user_info.generate_match_insights()
        return user_info.match_insights

    except Exception as e:
        print(e)
        return e

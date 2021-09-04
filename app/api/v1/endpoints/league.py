from fastapi import APIRouter
from ..middlewares.league_user_insights import UserInsights
from ..middlewares.league_stats import return_match_insight
from ..middlewares.league_user_info import get_user_info

router = APIRouter()


@router.get("/ping")
async def ping():
    """ Checking if server is alive or not"""
    return {"ping": "pong"}


@router.get("/find-user-info/{region}/{game_name}")
async def find_user_info(region: str, game_name: str):
    """ Finds relevant user information """
    info = get_user_info(region, game_name)
    if "status" not in info:
        return {
            "status": True,
            "info": info
        }
    else:
        return info


@router.get("/find-insights/{region}/{game_name}")
async def find_insights(region: str, game_name: str):
    """Finds recent match insights of user"""
    try:
        user_insights = UserInsights(region, game_name)
        user_insights.set_region_router()
        user_insights.set_puuid()
        if not user_insights.is_valid_user:
            return {
                "status": False,
                "message": f"User with the name, {user_insights.game_name} does not exist."
            }
        user_insights.get_match_history_id()
        if len(user_insights.match_history_ids) == 0:
            return {
                "status": False,
                "message": "No matches found."
            }
        user_insights.generate_match_insights()
        return user_insights.match_insights

    except Exception as e:
        print(e)
        return e

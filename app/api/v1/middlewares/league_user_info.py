import requests
import json
from .validator import is_valid_region
from ...constants import API_KEY


def get_user_info(region: str, game_name: str):
    """Gets neccessary user information"""
    if not is_valid_region(region):
        return {
            "status": False,
            "message": "Invalid region provided."
        }

    region_router = region.lower()
    url = f"https://{region_router}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{game_name}?api_key={API_KEY}"
    response = requests.request("GET", url, headers={}, data={})
    response = response.json()
    if "status" in response:
        return {
            "status": False,
            "message": f"User with the name, {game_name} does not exist."
        }
    return response

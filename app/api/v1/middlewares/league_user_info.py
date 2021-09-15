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

    encrypted_id = response["id"]
    url_additional = f"https://{region_router}.api.riotgames.com/lol/league/v4/entries/by-summoner/{encrypted_id}?api_key={API_KEY}"
    response_additional = requests.request(
        "GET", url_additional, headers={}, data={})
    response_additional = response_additional.json()
    if response_additional == []:
        return response
    response_additional = response_additional[0]
    response["leaguePoints"] = response_additional["leaguePoints"]
    response["wins"] = response_additional["wins"]
    response["losses"] = response_additional["losses"]
    response["totalGamesPlayed"] = response_additional["wins"] + \
        response_additional["losses"]
    response["winRate"] = round((response_additional["wins"]/(response_additional["wins"] + response_additional["losses"]))*100)
    response["tier"] = response_additional["tier"]
    response["rank"] = response_additional["rank"]

    return response

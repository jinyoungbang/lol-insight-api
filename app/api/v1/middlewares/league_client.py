import requests
import json
from .validator import is_valid_region

API_KEY = "RGAPI-f18f8105-1c10-4aa8-943e-a1b2148d2205"


def get_user_puuid(game_name, region):
    """Gets user's puuid
    Parameters
    ----------
    game_name: str, required
        User's in game name
    region: str, required
        User's region

    Returns
    ----------
    str:
        user's puuid
    """

    if not is_valid_region(region):
        return "Invalid region name."

    url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/" + \
        game_name + "/" + region + "?api_key=" + API_KEY
    payload, headers = {}, {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    return response["puuid"]


def get_match_history_id(puuid, start=0, count=20):
    """Gets match history id of a user
    Parameters
    ----------
    puuid: str, required
        User's puuid
    start: int, optional
        Most recent game
    count: int, optional
        The number of matches from start
    Returns
    ----------
    List[str]:
        List of match ids of users with given parameter
    """
    url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + \
        puuid + "/ids?start=" + start + "&count=" + count + "&api_key=" + API_KEY
    payload, headers = {}, {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    print(response.text)

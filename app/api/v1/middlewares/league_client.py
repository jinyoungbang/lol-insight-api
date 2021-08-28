import requests
import json
from .validator import is_valid_region

# https://developer.riotgames.com/
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
        puuid + "/ids?start=" + \
        str(start) + "&count=" + str(count) + "&api_key=" + API_KEY
    payload, headers = {}, {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    return response


def get_user_insights_from_match(match_id, puuid):
    """Gets user_specific from match id
    Parameters
    ----------
    match_id: str, required
        Match id
    puuid: str, required
        User's puuid

    Returns
    ----------
    Dict:
        Information of match id
    """
    match_id_splitted = match_id.split("_")
    match_region = match_id_splitted[0]
    match_id = match_id_splitted[1]

    url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + \
        match_region + "_" + match_id + "?api_key=" + API_KEY

    payload, headers = {}, {}
    response = requests.request("GET", url, headers=headers, data=payload)
    match_data = response.json()
    participants = match_data["metadata"]["participants"]

    if puuid not in participants:
        return {
            "status": False,
        }

    participant_index = participants.index(puuid)
    user_info = match_data["info"]["participants"][participant_index]
    return user_info


def get_insights_from_match(match_id):
    """Gets overall insight from match id
    Parameters
    ----------
    match_id: str, required
        Match id

    Returns
    ----------
    Dict:
        Information of match id
    """
    match_id_splitted = match_id.split("_")
    match_region = match_id_splitted[0]
    match_id = match_id_splitted[1]

    url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + \
        match_region + "_" + match_id + "?api_key=" + API_KEY

    payload, headers = {}, {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    return response

import requests
import json
from .validator import is_valid_region
from .league_stats import return_match_insight
from ...constants import API_KEY
import logging 

# https://developer.riotgames.com/
API_KEY = API_KEY


def _find_continent_routing(region):
    """Finds appropriate continent router based off of region
    Parameters
    ----------
    region: str, required
        User's region

    Returns
    ----------
    str:
        appropriate routing value
    """
    if region in ["NA1", "BR1", "LA1", "LA2", "OC1"]:
        return "americas"
    elif region in ["JP1", "KR"]:
        return "asia"
    else:
        return "europe"

def _find_region_routing(region):
    region_to_check = region.lower()
    valid_regions = {
        "br": "br1",
        "eun": "eun1",
        "euw": "euw1",
        "jp": "jp1",
        "kr": "kr",
        "lan": "la1",
        "las": "la2",
        "na": "na1",
        "oce": "oc1",
        "tr": "tr1",
        "ru": "ru"
    }
    if region in valid_regions:
        return valid_regions[region_to_check]
    return region_to_check



class UserInsights:
    def __init__(self, region: str, game_name: str):
        self.region = region
        self.region_router = ""
        self.continent_router = ""
        self.game_name = game_name
        self.is_valid_user = False
        self.account_id = ""
        self.puuid = ""
        self.match_history_ids = []
        self.match_insights = []
        self.summoner_level = 0

    def set_region_and_continent_router(self):
        """Sets the region router for API requests of user"""
        logging.info("Setting region router.")
        if not is_valid_region(self.region):
            return Exception("test")
        self.region_router = _find_region_routing(self.region)
        self.continent_router = _find_continent_routing(self.region)

    def set_puuid(self):
        """Sets user's puuid based on region and game_name"""
        logging.info("Setting user's puuid.")
        
        # Make API call to get user data
        url = f"https://{self.region_router}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{self.game_name}?api_key={API_KEY}"
        payload, headers = {}, {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()

        # If response is valid, set data to object
        if "status" not in response:
            self.is_valid_user = True
            self.puuid = response["puuid"]
            self.account_id = response["accountId"]
            self.summoner_level = response["summonerLevel"]

    def get_match_history_id(self, start=0, count=20):
        url = f"https://{self.continent_router}.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start={start}&count={count}&api_key={API_KEY}"
        payload, headers = {}, {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        self.match_history_ids = response

    def get_user_insight_from_match(self, match_id: str):
        match_id_splitted = match_id.split("_")
        match_region = match_id_splitted[0]
        match_id = match_id_splitted[1]
        url = f"https://{self.continent_router}.api.riotgames.com/lol/match/v5/matches/{match_region}_{match_id}?api_key={API_KEY}"
        payload, headers = {}, {}
        response = requests.request("GET", url, headers=headers, data=payload)
        match_data = response.json()
        participants = match_data["metadata"]["participants"]

        if self.puuid not in participants:
            return {
                "status": False,
            }

        participant_index = participants.index(self.puuid)
        user_info = match_data["info"]["participants"][participant_index]
        return user_info

    def generate_match_insights(self):
        match_insight_list = []
        counter = 0  # api limit
        for match_id in self.match_history_ids:
            match_insight = self.get_user_insight_from_match(match_id)
            match_insight = return_match_insight(match_insight)
            match_insight_list.append(match_insight)
            counter += 1
            if counter >= 5:
                break
        self.match_insights = match_insight_list

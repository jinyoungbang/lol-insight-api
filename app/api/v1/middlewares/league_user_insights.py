import requests
import json
from .validator import is_valid_region
from .league_stats import return_match_insight
from ...constants import API_KEY

# https://developer.riotgames.com/
API_KEY = API_KEY


def _find_region_routing(region):
    """Finds appropriate router based off of region
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


class UserInsights:
    def __init__(self, region, game_name):
        self.region = region
        self.region_router = ""
        self.game_name = game_name
        self.is_valid_user = False
        self.puuid = ""
        self.match_history_ids = []
        self.match_insights = []

    def set_region_router(self):
        """Sets the region router for API requests of user"""
        if not is_valid_region(self.region):
            return Exception("test")
        self.region_router = _find_region_routing(self.region)

    def set_puuid(self):
        """Sets user's puuid based on region and game_name"""
        url = f"https://{self.region_router}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{self.game_name}/{self.region}?api_key={API_KEY}"
        payload, headers = {}, {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        if "status" not in response:
            self.is_valid_user = True
            self.puuid = response["puuid"]

    def get_match_history_id(self, start=0, count=20):
        url = f"https://{self.region_router}.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start={start}&count={count}&api_key={API_KEY}"
        payload, headers = {}, {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        self.match_history_ids = response

    def get_user_insight_from_match(self, match_id):
        match_id_splitted = match_id.split("_")
        match_region = match_id_splitted[0]
        match_id = match_id_splitted[1]
        url = f"https://{self.region_router}.api.riotgames.com/lol/match/v5/matches/{match_region}_{match_id}?api_key={API_KEY}"
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

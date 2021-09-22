from fastapi import APIRouter
import logging
import json
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError

import config
from ..middlewares.league_user_insights import UserInsights
from ..middlewares.league_user_info import get_user_info
from ..middlewares.aws_dynamodb import DaivDynamoDB

router = APIRouter()

DYNAMODB_TABLE_NAME = config.DYNAMODB_TABLE_NAME


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
        # Initializes middleware objects
        user_insights = UserInsights(region, game_name)
        daiv_dynamodb = DaivDynamoDB(DYNAMODB_TABLE_NAME)

        # Sets region router for API requests based off of user's selected region.
        user_insights.set_region_and_continent_router()

        try:
            user_insights.set_puuid()
        except:
            logging.error("Unable to fetch puuid.")
            return {
                "msg": "Unable to fetch puuid."
            }

        # If user with given name does not exist, return error.
        if not user_insights.is_valid_user:
            return {
                "status": False,
                "message": f"User with the name, {user_insights.game_name} does not exist."
            }

        # If data in Database Cache, return it without calling Riot API.
        response = daiv_dynamodb.get_recent_matches(user_insights.puuid)
        if "Item" in response:
            return response["Item"]["matchData"][:20]
        else:
            print("Lambda cache unsuccessful.")

        # Retrieves recent match history and if none, return error.
        user_insights.get_match_history_id()
        if len(user_insights.match_history_ids) == 0:
            return []

        # Generate match insights for user
        user_insights.generate_match_insights()

        try:
            match_insights_dec = [{
                "insight": json.loads(json.dumps(insight["insight"]), parse_float=Decimal),
                "win": insight["win"],
                "userRole": insight["userRole"],
                "queueId": insight["queueId"],
                "matchId": insight["matchId"],
                "championName": insight["championName"],
                "kills": insight["kills"],
                "deaths": insight["deaths"],
                "assists": insight["assists"],
            } for insight in user_insights.match_insights]

            response = daiv_dynamodb.initialize_matches({
                "puuid": user_insights.puuid,
                "lastUpdatedMatchId": user_insights.match_history_ids[0],
                "matchData": match_insights_dec,
                "lastUpdated": datetime.utcnow().isoformat()
            })
        except Exception as e:
            print(e)

        return user_insights.match_insights

    except Exception as e:
        print(e)
        return e


@router.get("/refresh-insights/{region}/{game_name}")
async def refresh_insights(region: str, game_name: str):
    try:
        user = UserInsights(region, game_name)
        daiv_dynamodb = DaivDynamoDB(DYNAMODB_TABLE_NAME)

        # Sets region router for API requests based off of user's selected region.
        user.set_region_and_continent_router()

        # Sets user's puuid
        try:
            user.set_puuid()
        except:
            logging.error("Unable to fetch puuid.")
            return {
                "status": False,
                "msg": "Unable to fetch puuid."
            }

        # If user with given name does not exist, return error.
        if not user.is_valid_user:
            return {
                "status": False,
                "message": f"User with the name, {user.game_name} does not exist."
            }

        # Retrieves recent match history and if none, return error.
        user.get_match_history_id(start=0, count=50)
        if len(user.match_history_ids) == 0:
            return []

        # Retrieves most recent match id from the database.
        recent_match_id = daiv_dynamodb.get_recent_match_id(user.puuid)

        # If most recent match_id is in the match history, generate insights from news data to recent id.
        if recent_match_id in user.match_history_ids:
            num_data_to_generate = user.match_history_ids.index(
                recent_match_id)
            user.generate_match_insights(count=num_data_to_generate)

        # Convert float values to decimals to input in DynamoDB.
        match_insights_dec = [json.loads(json.dumps(
            insight), parse_float=Decimal) for insight in user.match_insights]

        # Appropriate format for match/insight data.
        match_data = [
            {
                "matchId": data,
                "matchType": None,
                "userRole": None,
                "insight": match_insights_dec[idx]
            } for (idx, data) in enumerate(user.match_history_ids[:num_data_to_generate])
        ]

        response = daiv_dynamodb.refresh_and_update_matches(
            user.puuid, match_data, user.match_history_ids[0])

        if not response["status"]:
            return response

        return {
            "status": True,
            "message": "Insights successfully updated."
        }

    except ClientError as err:
        if err.response["Error"]["Code"] == 'ConditionalCheckFailedException':
            raise ValueError("Doesn't exist") from err
        else:
            raise err

    except Exception as e:
        print(e)
        return e

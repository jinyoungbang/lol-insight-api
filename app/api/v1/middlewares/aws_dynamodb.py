from pprint import pprint
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


class DaivDynamoDB:
    def __init__(self, table_name: str = "daiv-dynamodb"):
        self.resource = boto3.resource('dynamodb')
        self.table = self.resource.Table(table_name)

    def get_recent_matches(self, puuid: str, num: int = 20):
        response = self.table.get_item(
            Key={
                "puuid": puuid
            }
        )
        return response

    def get_recent_match_id(self, puuid: str):
        response = self.table.get_item(
            Key={
                "puuid": puuid
            }
        )
        if "Item" not in response:
            return {
                "status": False,
                "msg": "Please initialize match data."
            }

        last_updated_match_id = response["Item"]["lastUpdatedMatchId"]
        return last_updated_match_id

    def initialize_matches(self, item: dict):
        response = self.table.put_item(
            Item=item
        )
        return response

    def refresh_last_updated_time(self, puuid: str):
        self.table.update_item(
            Key={
                'puuid': puuid,
            },
            UpdateExpression="SET lastUpdated = :value",
            ExpressionAttributeValues={
                ':value': datetime.utcnow().isoformat()
            },
            ReturnValues='UPDATED_NEW'
        )

        return {
            "status": True,
        }

    def refresh_and_update_matches(self, puuid: str, insights: list, recent_match_id: str):
        try:

            response = self.table.update_item(
                Key={
                    'puuid': puuid,
                },
                UpdateExpression="SET matchData = list_append(:md, matchData)",
                ExpressionAttributeValues={
                    ':md': insights,
                }
            )
            if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
                return {
                    "status": False,
                    "message": "Match append unsuccessful."
                }

            self.table.update_item(
                Key={
                    'puuid': puuid,
                },
                UpdateExpression="SET lastUpdatedMatchId = :value",
                ExpressionAttributeValues={
                    ':value': recent_match_id
                },
                ReturnValues='UPDATED_NEW'
            )

            self.table.update_item(
                Key={
                    'puuid': puuid,
                },
                UpdateExpression="SET lastUpdated = :value",
                ExpressionAttributeValues={
                    ':value': datetime.utcnow().isoformat()
                },
                ReturnValues='UPDATED_NEW'
            )

            return {
                "status": True,
            }

        except ClientError as err:
            if err.response["Error"]["Code"] == 'ConditionalCheckFailedException':
                return ValueError("Doesn't exist")
            else:
                return err

from pprint import pprint
from datetime import datetime
import time
import json
import boto3
from botocore.exceptions import ClientError


class S3:
    def __init__(self, bucket_name: str):
        self.client = boto3.client('s3')
        self.bucket_name = bucket_name

    def put_json_object(self, key: str, data: dict):
        json_object = data
        self.client.put_object(
            Body=json.dumps(json_object),
            Bucket=self.bucket_name,
            Key=key
        )
        return

    def fetch_json_object(self, key: str):
        response = self.client.get_object(
            Bucket=self.bucket_name, 
            Key=key
        )
        data = json.loads(response["Body"].read().decode())
        return data

# Flask Configuration file
import os
from dotenv import load_dotenv

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

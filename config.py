from dotenv import load_dotenv
import os

load_dotenv()

class Secrets:
    def __init__(self):
        self.API_key = os.getenv("API_KEY")
        self.API_key_secret = os.getenv("API_KEY_SECRET")
        self.bearer_token = os.getenv("BEARER_TOKEN")
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.access_secret = os.getenv("ACCESS_SECRET")

import json
from dotenv import load_dotenv
import os

load_dotenv()


def load_config():
    with open('data/config.json', 'r') as f:
        return json.load(f)


config = load_config()

role_ping = config["role_ping"]
forum_channel_id = config["forum_channel_id"]
discord_token = os.getenv("TOKEN")

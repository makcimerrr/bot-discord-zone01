import json
from dotenv import load_dotenv
import os

load_dotenv()


def load_config():
    with open('data/config.json', 'r') as f:
        return json.load(f)


config = load_config()

role_ping = config["role_ping"]
role_ping_cdi = config["role_ping_cdi"]
forum_channel_id = config["forum_channel_id"]
forum_channel_id_cdi = config["forum_channel_id_cdi"]
guild_id = config["guild_id"]
discord_token = os.getenv("TOKEN")

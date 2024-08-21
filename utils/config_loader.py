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
role_p1_2023 = config["role_p1_2023"]
role_p2_2023 = config["role_p2_2023"]
role_p1_2024 = config["role_p1_2024"]
role_help = config["role_help"]
discord_token = os.getenv("TOKEN")

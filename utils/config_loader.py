import json
from pathlib import Path

from dotenv import load_dotenv
import os

# Spécifiez le chemin du fichier .env, par exemple dans le dossier racine
env_path = Path('../.env')  # Charger le fichier .env situé dans le répertoire parent
load_dotenv(dotenv_path=env_path, override=True)
def load_config():
    with open('data/config.json', 'r') as f:
        return json.load(f)


def load_technologies():
    with open('data/technologies.json', 'r') as f:
        return json.load(f)


config = load_config()
techs = load_technologies()

# Variables

technologies = techs["technologies"]
role_ping_cdi = config["role_ping_cdi"]
forum_channel_id = config["forum_channel_id"]
forum_channel_id_cdi = config["forum_channel_id_cdi"]
guild_id = config["guild_id"]
role_p1_2023 = config["role_p1_2023"]
role_p2_2023 = config["role_p2_2023"]
role_p1_2024 = config["role_p1_2024"]
role_help = config["role_help"]
role_ping_alternance = config["role_ping_alternance"]
channel_inter_promo = config["channel_inter_promo"]
discord_token = os.getenv("TOKEN")
query_intern = os.getenv("QUERY_INTERNSHIP")
query_fulltime = os.getenv("QUERY_FULLTIME")
channel_progress_P1_2022 = config["channel_progress_P1_2022"]
channel_progress_P1_2023 = config["channel_progress_P1_2023"]
channel_progress_P2_2023 = config["channel_progress_P2_2023"]
channel_progress_P1_2024 = config["channel_progress_P1_2024"]
channel_progress_P1_2025 = config["channel_progress_P1_2025"]
forbidden_words = ["Openclassrooms", "MyDigitalSchool", "ISCOD", "EPSI", "2I Academy", "Studi CFA"]
channel_id_feedback_alternance = int(os.getenv('CHANNEL_ID', 0)) if os.getenv('CHANNEL_ID') else None
role_feedback_alternance = int(os.getenv('ROLE_ID', 0)) if os.getenv('ROLE_ID') else None
notion_token = os.getenv("NOTION_TOKEN")
notion_database_id = os.getenv("NOTION_DATABASE_ID")

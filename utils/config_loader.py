import os

import aiohttp
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path('../.env')
load_dotenv(dotenv_path=env_path, override=True)

API_URL = os.getenv("CONFIG_API_URL")


# ---------- Config Discord (ID rôles, channels, etc.) ----------

async def fetch_config_value(key: str):
    """Récupère une valeur spécifique de config Discord depuis l'API de manière asynchrone."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/discord/{key}/config") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("value")  # on cible la valeur dans la réponse
                else:
                    print(f"[Config] Erreur API pour '{key}' : status {resp.status}")
                    return None
    except Exception as e:
        print(f"[Config Async] Erreur pour '{key}' : {e}")
        return None


async def fetch_full_config():
    """Récupère toute la configuration Discord depuis l'API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/discord/config/full") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("config", {})
                else:
                    print(f"[Full Config] Erreur API : status {resp.status}")
                    return {}
    except Exception as e:
        print(f"[Full Config Async] Erreur : {e}")
        return {}

# ---------- Technologies ----------

async def fetch_technologies():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/discord/technologies") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["technologies"]
                else:
                    print(f"Erreur API : {resp.status}")
                    return []
    except Exception as e:
        print(f"Erreur réseau : {e}")
        return []


# ---------- Forbidden Words ----------

async def fetch_forbidden_schools():
    """Récupère la liste des écoles interdites depuis l'API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/discord/forbidden-schools") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("schools", [])
                else:
                    print(f"[Forbidden Schools] Erreur API : status {resp.status}")
                    return []
    except Exception as e:
        print(f"[Forbidden Schools] Exception: {e}")
        return []

# ---------- Variables d’environnement ----------

def get_token():
    return os.getenv("TOKEN")


def get_query_intern():
    return os.getenv("QUERY_INTERNSHIP")


def get_query_fulltime():
    return os.getenv("QUERY_FULLTIME")

async def fetch_job_queries():
    """Récupère toutes les requêtes d'emploi depuis l'API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/discord/job-queries") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("queries", [])
                else:
                    print(f"Erreur API job_queries: {resp.status}")
                    return []
    except Exception as e:
        print(f"[JobQueries] Erreur: {e}")
        return []

class JobQuery:
    def __init__(self, data: Dict[str, Any]):
        self.query = data.get("query")
        self.page = data.get("page")
        self.num_pages = data.get("num_pages")
        self.country = data.get("country")
        self.date_posted = data.get("date_posted")
        self.employment_types = data.get("employment_types")
        self.radius = data.get("radius")
        self.created_at = data.get("created_at")

    def __repr__(self):
        return (
            f"<JobQuery {self.query}: page={self.page}, num_pages={self.num_pages}, "
            f"country={self.country}, date_posted={self.date_posted}, "
            f"employment_types={self.employment_types}, radius={self.radius}>"
        )

async def fetch_job_query_details(query_name: str) -> Optional[JobQuery]:
    """Récupère les détails d'une requête d'emploi spécifique par son nom"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/job-queries") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    queries = data.get("queries", [])
                    for q in queries:
                        if q.get("query") == query_name:
                            return JobQuery(q)
                    print(f"⚠️ Query '{query_name}' introuvable.")
                else:
                    print(f"Erreur API job_queries: {resp.status}")
    except Exception as e:
        print(f"[JobQuery Fetch] Erreur pour '{query_name}': {e}")

    return None


discord_token = get_token()
technologies = fetch_technologies()
forbidden_words = fetch_forbidden_schools()
forum_channel_id = fetch_config_value("forum_channel_id")
forum_channel_id_cdi = fetch_config_value("forum_channel_id_cdi")
role_ping_cdi = fetch_config_value("role_ping_cdi")
role_ping_intern = fetch_config_value("role_ping_intern")
role_ping_fulltime = fetch_config_value("role_ping_fulltime")
role_ping_alternance = fetch_config_value("role_ping_intern")
role_ping_internship = fetch_config_value("role_ping_internship")
guild_id = fetch_config_value("guild_id")
config = {
    "discord_token": discord_token,
    "query_intern": get_query_intern(),
    "query_fulltime": get_query_fulltime(),
    "forum_channel_id": forum_channel_id,
    "forum_channel_id_cdi": forum_channel_id_cdi,
    "role_ping_cdi": role_ping_cdi,
    "role_ping_intern": role_ping_intern,
    "role_ping_fulltime": role_ping_fulltime,
    "role_ping_internship": role_ping_internship,
    "role_ping_alternance": role_ping_alternance,
    "guild_id": guild_id
}

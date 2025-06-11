import aiohttp
import os
from typing import Tuple, Optional, List
from utils.config_loader import fetch_job_query_details


async def fetch_api_fulltime(bot) -> Tuple[List[dict], Optional[str], Optional[Exception]]:
    """
    Récupère les offres d'emploi full-time en utilisant la configuration dynamique
    depuis l'API (query_fulltime).
    """
    # Récupération dynamique de la configuration de la query
    query = await fetch_job_query_details("query_fulltime")

    if query is None or not query.query:
        print("❌ Aucune query_fulltime définie dans la base de données.")
        return [], "Aucune query définie", None

    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": query.query,
        "page": str(query.page or 1),
        "num_pages": str(query.num_pages or 10),
        "country": query.country or "fr",
        "date_posted": query.date_posted or "today",
        "employment_types": query.employment_types or "FULLTIME",
        "radius": str(query.radius or 50),
    }

    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as resp:
                resp.raise_for_status()
                result = await resp.json()
                data = result.get("data", [])
                return data if isinstance(data, list) else [], query.query, None
    except Exception as e:
        print(f"❌ Erreur JSearch: {e}")
        return [], query.query, e
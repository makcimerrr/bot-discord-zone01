import os
from pathlib import Path

import requests
from dotenv import load_dotenv


async def fetch_api_fulltime(bot):
    """# On récupère le Cog QueryCog depuis l'instance du bot
    query_cog = bot.get_cog('QueryCog')

    # Vérifier si le Cog est bien chargé
    if query_cog is None:
        print("Le Cog QueryCog n'est pas chargé.")
        return [], "Le Cog QueryCog n'est pas chargé"

    # Obtenir la valeur de query_fulltime à partir du Cog
    query_fulltime = query_cog.get_query_fulltime()"""

    env_path = Path('../.env')  # Charger le fichier .env situé à la racine du projet
    load_dotenv(dotenv_path=env_path, override=True)
    query_fulltime = os.getenv('QUERY_FULLTIME')

    # Vérifier si une query a été définie
    if query_fulltime is None or query_fulltime == "":
        print("Aucune query n'a été définie.")
        return [], "Aucune query n'a été définie", None

    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {"query": query_fulltime, "page": "1", "num_pages": "1", "country": "fr", "date_posted": "today",
                   "employment_types": "FULLTIME", "radius": "200"}

    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json().get('data', [])
        return data if isinstance(data, list) else [], query_fulltime, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSearch jobs: {e}")
        return [], query_fulltime, e

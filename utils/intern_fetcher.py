import os
import requests


async def fetch_api_intern():
    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {"query": "full stack developer alternant in rouen, france", "page": "1", "num_pages": "1", "date_posted": "today",
                   "employment_types": "INTERN", "radius": "70"}

    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json().get('data', [])
        return data if isinstance(data, list) else []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSearch jobs: {e}")
        return []

import os
import requests


def fetch_linkedin_cdi():
    url = "https://linkedin-data-api.p.rapidapi.com/search-jobs"

    querystring = {"keywords": "Developer", "locationId": "100546625", "datePosted": "pastWeek",
                   "jobType": "fullTime, contract, partTime", "titleIds": "24&", "sort": "mostRelevant"}

    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY2'),
        "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Indeed details jobs: {e}")
        return []


def fetch_indeed_cdi():
    url = "https://indeed12.p.rapidapi.com/jobs/search"

    querystring = {"query": "developer", "location": "rouen", "page_id": "1", "locality": "fr", "fromage": "1",
                   "radius": "120", "sort": "date"}

    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY2'),
        "x-rapidapi-host": "indeed12.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        jobs = response.json().get('hits', [])
        return jobs if isinstance(jobs, list) else []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Indeed jobs: {e}")
        return []
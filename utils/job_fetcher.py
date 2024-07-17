import os
import requests


# Function to fetch jobs from JSearch API
def fetch_new_jobs():
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {
        "query": "Developer fullstack in rouen, France",
        "page": "1",
        "num_pages": "1",
        "date_posted": "week",
        "employment_types": "INTERN",
        "radius": "120"
    }
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


# Function to fetch jobs from LinkedIn Jobs Search API
def fetch_linkedin_jobs():
    url = "https://linkedin-jobs-search.p.rapidapi.com/"
    payload = {
        "search_terms": "Alternance_Développeur",
        "location": "Rouen, France",
        "radius": "120",
        "page": "1",
        "employment_type": ["INTERN"]
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY'),
        "X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        jobs = response.json()
        if isinstance(jobs, list):
            return jobs
        elif isinstance(jobs, dict):
            return jobs.get('jobs', [])
        else:
            print(f"Unexpected response type from LinkedIn API: {type(jobs)}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching LinkedIn jobs: {e}")
        return []


# Function to fetch jobs from Indeed API
def fetch_indeed_jobs():
    url = "https://indeed12.p.rapidapi.com/jobs/search"
    querystring = {
        "query": "alternant développeur",
        "location": "rouen",
        "page_id": "1",
        "locality": "fr",
        "fromage": "1",
        "radius": "120",
        "sort": "date"
    }
    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
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

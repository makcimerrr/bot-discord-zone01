import requests
import os

def get_details_indeed(job_id):
    url = f"https://indeed12.p.rapidapi.com/job/{job_id}"
    querystring = {"locality": "fr"}

    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY2'),
        "x-rapidapi-host": "indeed12.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Parse JSON from the response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Indeed job details: {e}")
        return None  # Return None if there's an error

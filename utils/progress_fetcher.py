import requests


async def fetch_progress():
    url = "https://admin-dashboard-blue-one.vercel.app/api/timeline_project"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching progress: {e}")
        return None

import aiohttp


async def fetch_progress():
    url = "https://admin-dashboard-blue-one.vercel.app/api/timeline_project"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return data
    except aiohttp.ClientError as e:
        print(f"Error fetching progress: {e}")
        return None

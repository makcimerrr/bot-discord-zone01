import aiohttp


async def get_departement(ville):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://geo.api.gouv.fr/communes?nom={ville}&fields=departement&format=json") as response:
                data = await response.json()

                if data:
                    # On récupère le département associé à la ville
                    return data[0]['departement']['nom']
                else:
                    return None
    except aiohttp.ClientError:
        return None

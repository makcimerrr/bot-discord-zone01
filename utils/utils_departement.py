import requests


def get_departement(ville):
    response = requests.get(f"https://geo.api.gouv.fr/communes?nom={ville}&fields=departement&format=json")
    data = response.json()

    if data:
        # On récupère le département associé à la ville
        return data[0]['departement']['nom']
    else:
        return None

import requests
import json

# Configuration des URLs et des en-têtes
search_url = "https://api.coresignal.com/cdapi/v1/linkedin/job/search/filter"
collect_url_template = "https://api.coresignal.com/cdapi/v1/linkedin/job/collect/{}"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJFZERTQSIsImtpZCI6IjFkMTA5NzVmLWExNWItYzgwMS0xMjZkLWE5YjhlYTJlMWU2MiJ9'
                     '.eyJhdWQiOiJjc21yb3Vlbi5uZXQiLCJleHAiOjE3NTMzOTkwMjEsImlhdCI6MTcyMTg0MjA2OSwiaXNzIjoiaHR0cHM6Ly9vcHMuY29yZXNpZ25hbC5jb206ODMwMC92MS9pZGVudGl0eS9vaWRjIiwibmFtZXNwYWNlIjoicm9vdCIsInByZWZlcnJlZF91c2VybmFtZSI6ImNzbXJvdWVuLm5ldCIsInN1YiI6ImZhMGM0YzljLWMyMWMtZmZkZi1jMGI5LTQ4YWVkNWFmOWMxNiIsInVzZXJpbmZvIjp7InNjb3BlcyI6ImNkYXBpIn19.Vg1lkZr2M7pArHPQ2ikBzA9qftAPvmhfyZcFouaKNEHuTKFbaZeuh2tnfGunfie-qI7sp0PMqUZW4M_7bBeABQ'
}

# Payload pour la recherche initiale
search_payload = json.dumps({
    "title": "(Full Stack Developer)",
    "application_active": "True",
    "deleted": "False",
    "country": "France",
    "employment_type": "Full-time"
})

# Effectuer la recherche initiale pour obtenir les identifiants des offres d'emploi
search_response = requests.post(search_url, headers=headers, data=search_payload)

# Vérifier si la réponse de la recherche initiale est valide
if search_response.status_code == 200:
    job_ids = search_response.json()  # Extraire les identifiants d'emploi de la réponse

    with open("job_details.txt", "w", encoding="utf-8") as file:
        for job_id in job_ids:
            # Construire l'URL pour collecter les détails de l'offre d'emploi
            collect_url = collect_url_template.format(job_id)

            # Effectuer la requête pour collecter les détails de l'offre d'emploi
            collect_response = requests.get(collect_url, headers=headers)

            # Vérifier si la réponse de la collecte des détails est valide
            if collect_response.status_code == 200:
                job_details = collect_response.json()  # Extraire les détails de l'offre d'emploi

                # Récupérer les informations spécifiques
                time_posted = job_details.get("time_posted", "N/A")
                title = job_details.get("title", "N/A")
                location = job_details.get("location", "N/A")
                url = job_details.get("url", "N/A")
                company_name = job_details.get("company_name", "N/A")

                # Écrire les informations dans le fichier
                file.write(f"time_posted: {time_posted}\n")
                file.write(f"title: {title}\n")
                file.write(f"location: {location}\n")
                file.write(f"url: {url}\n")
                file.write(f"company_name: {company_name}\n")
                file.write("==========\n")
            else:
                print(
                    f"Erreur lors de la collecte des détails de l'offre d'emploi {job_id}: {collect_response.status_code}")
else:
    print(f"Erreur lors de la recherche initiale: {search_response.status_code}")

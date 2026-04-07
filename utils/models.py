from notion_client import Client
from datetime import datetime, timedelta
from dotenv import load_dotenv
from utils.config_loader import notion_database_id, notion_token

load_dotenv(override=True)

if not notion_token:
    print("⚠️ NOTION_TOKEN non défini dans .env — l'enregistrement des réponses sera désactivé.")
if not notion_database_id:
    print("⚠️ NOTION_DATABASE_ID non défini dans .env — l'enregistrement des réponses sera désactivé.")

notion = Client(auth=notion_token) if notion_token else None

def get_first_monday_of_month(reference_date=None):
    """Retourne le premier lundi du mois (UTC)"""
    if reference_date is None:
        reference_date = datetime.utcnow()

    first_day = reference_date.replace(day=1)
    days_to_monday = (7 - first_day.weekday()) % 7
    first_monday = first_day + timedelta(days=days_to_monday)
    return first_monday.replace(hour=0, minute=0, second=0, microsecond=0)

def add_response_to_notion(user, response):
    if not notion or not notion_database_id:
        raise RuntimeError("Notion non configuré (NOTION_TOKEN ou NOTION_DATABASE_ID manquant)")

    today = datetime.utcnow()
    first_monday = get_first_monday_of_month(today)

    # Format de la colonne mensuelle
    date_column = first_monday.strftime("Mois du %d/%m/%Y")

    # Création de la colonne si elle n'existe pas (on essaie directement)
    try:
        notion.request(
            path=f"databases/{notion_database_id}",
            method="PATCH",
            body={
                "properties": {
                    date_column: {
                        "rich_text": {}
                    }
                }
            }
        )
    except Exception as e:
        # La colonne existe peut-être déjà, on continue
        print(f"[DEBUG] Création colonne (ignoré si existe déjà): {e}")

    # Recherche de l'utilisateur existant
    results = notion.request(
        path=f"databases/{notion_database_id}/query",
        method="POST",
        body={
            "filter": {
                "property": "pseudo",
                "title": {
                    "equals": user
                }
            }
        }
    )

    try:
        if not results['results']:
            # Création de l'utilisateur si inexistant
            notion.request(
                path="pages",
                method="POST",
                body={
                    "parent": {"database_id": notion_database_id},
                    "properties": {
                        "pseudo": {
                            "title": [{"text": {"content": user}}]
                        },
                        "Last Updated": {
                            "date": {"start": datetime.utcnow().isoformat()}
                        },
                        date_column: {
                            "rich_text": [{"text": {"content": response}}]
                        }
                    }
                }
            )
        else:
            # Mise à jour de la ligne existante
            page_id = results['results'][0]['id']
            notion.request(
                path=f"pages/{page_id}",
                method="PATCH",
                body={
                    "properties": {
                        "Last Updated": {
                            "date": {"start": datetime.utcnow().isoformat()}
                        },
                        date_column: {
                            "rich_text": [{"text": {"content": response}}]
                        }
                    }
                }
            )
    except Exception as e:
        print(f"Erreur lors de la mise à jour : {e}")
        raise

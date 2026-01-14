from notion_client import Client
from datetime import datetime, timedelta
from dotenv import load_dotenv
from utils.config_loader import notion_database_id, notion_token

load_dotenv(override=True)

notion = Client(auth=notion_token)

def get_first_monday_of_month(reference_date=None):
    """Retourne le premier lundi du mois (UTC)"""
    if reference_date is None:
        reference_date = datetime.utcnow()

    first_day = reference_date.replace(day=1)
    days_to_monday = (7 - first_day.weekday()) % 7
    first_monday = first_day + timedelta(days=days_to_monday)
    return first_monday.replace(hour=0, minute=0, second=0, microsecond=0)

def add_response_to_notion(user, response):
    today = datetime.utcnow()
    first_monday = get_first_monday_of_month(today)

    # Format de la colonne mensuelle
    date_column = first_monday.strftime("Mois du %d/%m/%Y")

    # Récupération de la base de données
    print(f"[DEBUG] notion_database_id: {notion_database_id}")
    database = notion.databases.retrieve(database_id=notion_database_id)
    print(f"[DEBUG] database response keys: {database.keys() if database else 'None'}")

    # Création de la colonne si elle n'existe pas
    if date_column not in database.get('properties', {}):
        try:
            notion.databases.update(
                database_id=notion_database_id,
                properties={
                    date_column: {
                        "rich_text": {}
                    }
                }
            )
        except Exception as e:
            print(f"Erreur lors de la création de la colonne : {e}")
            raise

    # Recherche de l'utilisateur existant
    results = notion.databases.query(
        database_id=notion_database_id,
        filter={
            "property": "pseudo",
            "title": {
                "equals": user
            }
        }
    )

    try:
        if not results['results']:
            # Création de l'utilisateur si inexistant
            notion.pages.create(
                parent={"database_id": notion_database_id},
                properties={
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
            )
        else:
            # Mise à jour de la ligne existante
            page_id = results['results'][0]['id']
            notion.pages.update(
                page_id=page_id,
                properties={
                    "Last Updated": {
                        "date": {"start": datetime.utcnow().isoformat()}
                    },
                    date_column: {
                        "rich_text": [{"text": {"content": response}}]
                    }
                }
            )
    except Exception as e:
        print(f"Erreur lors de la mise à jour : {e}")
        raise
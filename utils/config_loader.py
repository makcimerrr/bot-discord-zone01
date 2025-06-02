import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path('../.env')
load_dotenv(dotenv_path=env_path, override=True)

API_URL = os.getenv("CONFIG_API_URL")  # Exemple : http://localhost:8000

# ---------- Config Discord (ID rôles, channels, etc.) ----------

def get_config_value(key: str):
    """Récupère une valeur spécifique de config Discord depuis l'API"""
    try:
        response = requests.get(f"{API_URL}/config")
        response.raise_for_status()
        return response.json().get(key)
    except Exception as e:
        print(f"[Config] Erreur pour '{key}' : {e}")
        return None

# Exemple d’utilisation : get_config_value("role_ping_cdi")

# ---------- Technologies ----------

def get_technologies():
    try:
        response = requests.get(f"{API_URL}/technologies")
        response.raise_for_status()
        return response.json().get("technologies", [])
    except Exception as e:
        print(f"[Technologies] Erreur : {e}")
        return []

# Exemple : get_technologies()

# ---------- Forbidden Words ----------

def get_forbidden_words():
    try:
        response = requests.get(f"{API_URL}/forbidden-words")
        response.raise_for_status()
        return response.json().get("forbidden_words", [])
    except Exception as e:
        print(f"[Forbidden Words] Erreur : {e}")
        return []

# Exemple : get_forbidden_words()

# ---------- Variables d’environnement ----------

def get_token():
    return os.getenv("TOKEN")

def get_query_intern():
    return os.getenv("QUERY_INTERNSHIP")

def get_query_fulltime():
    return os.getenv("QUERY_FULLTIME")
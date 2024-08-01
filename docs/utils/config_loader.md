# Documentation pour le module config_loader

## Description

La fonction `load_config` est utilisée pour charger et lire les paramètres de configuration depuis un fichier JSON. Ces paramètres sont ensuite utilisés pour configurer des variables globales nécessaires au fonctionnement d'une application.

## Détails de l'implémentation

- **Fichier de configuration** : `data/config.json`
- **Format du fichier** : JSON

## Fonctionnalité

1. **Chargement du fichier de configuration** :
   - La fonction ouvre le fichier `data/config.json` en mode lecture.
   - Elle utilise la bibliothèque `json` pour lire le contenu du fichier et le convertir en dictionnaire Python.

2. **Retour des données** :
   - La fonction retourne le dictionnaire Python chargé à partir du fichier JSON.

## Variables globales

Après l'appel à `load_config`, les variables globales suivantes sont définies en utilisant les données du fichier de configuration et des variables d'environnement :

- `role_ping` : Valeur extraite de `config["role_ping"]`
- `role_ping_cdi` : Valeur extraite de `config["role_ping_cdi"]`
- `forum_channel_id` : Valeur extraite de `config["forum_channel_id"]`
- `forum_channel_id_cdi` : Valeur extraite de `config["forum_channel_id_cdi"]`
- `guild_id` : Valeur extraite de `config["guild_id"]`
- `discord_token` : Valeur de la variable d'environnement `TOKEN`, obtenue via `os.getenv("TOKEN")`

## Exemples d'utilisation

```python
# Charger les configurations
config = load_config()

# Accéder aux paramètres de configuration
print(config["role_ping"])
print(config["forum_channel_id"])

# Accéder aux variables globales
print(role_ping)
print(discord_token)
```

## Gestion des erreurs

- La fonction `load_config` suppose que le fichier `data/config.json` existe et est bien formé. En cas d'absence du fichier ou de format incorrect, des exceptions (`FileNotFoundError`, `json.JSONDecodeError`) peuvent être levées.
- La variable d'environnement `TOKEN` doit être définie pour obtenir le jeton Discord. Sinon, `discord_token` sera `None`.

## Remarques

- **Dépendances** :
  - `python-dotenv` : Utilisé pour charger les variables d'environnement depuis un fichier `.env`.
  - `json` : Utilisé pour lire les données du fichier de configuration en format JSON.

- **Fichier `.env`** :
  - Assurez-vous que le fichier `.env` est présent et contient la variable `TOKEN` avec une clé valide pour l'application Discord.

- **Chemin du fichier** :
  - Le fichier de configuration est supposé être situé dans le répertoire `data`. Modifiez le chemin si le fichier est stocké ailleurs.


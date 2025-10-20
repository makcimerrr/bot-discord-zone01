# Système de Logging Centralisé

## Description

Le bot Discord Zone01 utilise un système de logging centralisé qui enregistre tous les événements du bot dans des fichiers JSON et les affiche dans l'interface web. **Aucun log n'est affiché dans le terminal** pour alléger la charge sur le serveur.

## Pourquoi ce système ?

- **Performance** : Pas d'affichage dans le terminal = moins de charge CPU
- **Traçabilité** : Tous les logs sont sauvegardés dans un fichier JSON
- **Visualisation** : Interface web moderne pour consulter les logs
- **Filtrage** : Filtrer par niveau, catégorie, limite
- **Statistiques** : Vue d'ensemble du nombre de logs par type

## Architecture

### Fichiers

```
utils/logger.py          # Module de logging centralisé
data/bot_logs.json       # Fichier de stockage des logs
templates/logs.html      # Page web pour visualiser les logs
```

### Module Logger (utils/logger.py)

Le module `logger.py` fournit une classe `BotLogger` avec les méthodes suivantes :

```python
from utils.logger import logger

# Méthodes disponibles
logger.info("Message d'information", category="bot")
logger.success("Opération réussie", category="bot")
logger.warning("Avertissement", category="bot")
logger.error("Erreur critique", category="bot")
logger.debug("Message de débogage", category="bot")
```

### Niveaux de Log

| Niveau | Icône | Couleur | Utilisation |
|--------|-------|---------|-------------|
| INFO | ℹ️ | Bleu | Informations générales |
| SUCCESS | ✅ | Vert | Opération réussie |
| WARNING | ⚠️ | Orange | Avertissement |
| ERROR | ❌ | Rouge | Erreur critique |
| DEBUG | 🐛 | Gris | Débogage |

### Catégories de Log

Les logs sont organisés par catégories pour faciliter le filtrage :

- **bot** : Événements du bot (démarrage, connexion, déconnexion)
- **cog** : Chargement des cogs/extensions
- **help_system** : Système d'aide par réaction
- **help_button** : Système d'aide par bouton
- **notion** : Intégration Notion
- **web** : Interface web
- **general** : Catégorie par défaut

## Utilisation dans le Code

### Dans un cog

```python
from utils.logger import logger

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.success("MyCog chargé", category="cog")

    @commands.command()
    async def my_command(self, ctx):
        try:
            # Votre code ici
            logger.info("Commande exécutée avec succès", category="cog")
        except Exception as e:
            logger.error(f"Erreur dans my_command : {e}", category="cog")
```

### Dans le bot principal

```python
from utils.logger import logger

# Remplacer print() par logger
# Avant
print("Bot is ready")

# Après
logger.success("Bot Discord démarré avec succès", category="bot")
```

## Interface Web

### Page des Logs

Accessible sur : `http://localhost:5000/logs`

**Fonctionnalités :**

1. **Statistiques en temps réel**
   - Total des logs
   - Nombre de logs par niveau (INFO, SUCCESS, WARNING, ERROR, DEBUG)

2. **Filtres**
   - Filtrer par niveau (INFO, SUCCESS, WARNING, ERROR, DEBUG)
   - Filtrer par catégorie (bot, cog, help_system, etc.)
   - Limiter le nombre de logs affichés (50, 100, 200, 500)

3. **Liste des logs**
   - Date/Heure de chaque log
   - Niveau avec badge coloré
   - Catégorie
   - Message du log

4. **Actions**
   - Actualiser les logs
   - Effacer tous les logs
   - Actualisation automatique toutes les 15 secondes

### Captures d'Écran

La page de logs affiche :
- Statistiques en haut (cartes colorées par niveau)
- Formulaire de filtrage
- Table des logs avec scroll
- Légende des niveaux

## API REST

### GET `/api/logs`

Récupère les logs avec filtres optionnels.

**Paramètres de requête :**
- `level` : Filtrer par niveau (INFO, SUCCESS, WARNING, ERROR, DEBUG)
- `category` : Filtrer par catégorie
- `limit` : Nombre maximum de logs (défaut: 100)

**Exemple :**
```
GET /api/logs?level=ERROR&category=bot&limit=50
```

**Réponse :**
```json
[
  {
    "timestamp": "2025-01-20T10:30:00.000000",
    "level": "ERROR",
    "category": "bot",
    "message": "Erreur lors de la synchronisation des commandes"
  }
]
```

### GET `/api/logs/stats`

Récupère les statistiques des logs.

**Réponse :**
```json
{
  "total": 245,
  "info": 120,
  "success": 80,
  "warning": 30,
  "error": 10,
  "debug": 5
}
```

### POST `/api/logs/clear`

Efface tous les logs.

**Réponse :**
```json
{
  "success": true,
  "message": "Logs effacés"
}
```

## Configuration

### Limite de logs en mémoire

Par défaut, le logger garde **500 logs** en mémoire. Cette limite peut être modifiée dans `utils/logger.py` :

```python
MAX_LOGS_IN_MEMORY = 500  # Modifier cette valeur
```

### Désactivation des logs Discord.py

Les logs de la bibliothèque `discord.py` sont désactivés dans le terminal pour éviter le bruit. Cela est configuré dans `bot.py` :

```python
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.getLogger('discord.http').setLevel(logging.CRITICAL)
logging.getLogger('discord.gateway').setLevel(logging.CRITICAL)
```

### Désactivation des logs Flask

Les logs du serveur Flask sont également désactivés dans `web_interface.py` :

```python
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
```

## Stockage des Logs

Les logs sont stockés dans `data/bot_logs.json` au format JSON :

```json
[
  {
    "timestamp": "2025-01-20T10:30:00.000000",
    "level": "SUCCESS",
    "category": "bot",
    "message": "Bot Discord démarré avec succès"
  },
  {
    "timestamp": "2025-01-20T10:30:05.123456",
    "level": "INFO",
    "category": "help_system",
    "message": "Helper John a accepté d'aider Alice"
  }
]
```

## Avantages du Système

1. **Performance** ✅
   - Pas d'affichage dans le terminal
   - Moins de charge CPU
   - Meilleure performance sur serveur

2. **Traçabilité** ✅
   - Tous les logs sont sauvegardés
   - Historique complet des événements
   - Facile à archiver

3. **Visualisation** ✅
   - Interface web moderne
   - Filtrage puissant
   - Statistiques en temps réel

4. **Maintenance** ✅
   - Débogage facilité
   - Détection rapide des erreurs
   - Analyse des performances

## Bonnes Pratiques

### 1. Choisir le bon niveau

```python
# INFO : Informations générales
logger.info("Utilisateur a exécuté la commande !ping", category="bot")

# SUCCESS : Opération réussie
logger.success("Extension chargée : cogs.administration_cog", category="bot")

# WARNING : Quelque chose d'anormal mais non critique
logger.warning("Impossible d'envoyer un MP à l'utilisateur", category="help_system")

# ERROR : Erreur critique
logger.error("Échec de la connexion à la base de données", category="bot")

# DEBUG : Informations de débogage (désactiver en production)
logger.debug(f"Variables : user={user}, guild={guild}", category="bot")
```

### 2. Utiliser des catégories cohérentes

```python
# Bon
logger.info("Message", category="bot")
logger.info("Message", category="help_system")

# Mauvais
logger.info("Message", category="Bot")  # Incohérent (majuscule)
logger.info("Message", category="help system")  # Mauvais (espace)
```

### 3. Messages clairs et descriptifs

```python
# Bon
logger.success("Helper John a accepté d'aider Alice", category="help_system")

# Mauvais
logger.success("OK", category="help_system")
```

## Dépannage

### Les logs ne s'affichent pas dans l'interface web

1. Vérifiez que le fichier `data/bot_logs.json` existe
2. Vérifiez les permissions du fichier
3. Actualisez la page des logs

### Erreur "No module named 'utils.logger'"

Assurez-vous que le fichier `utils/logger.py` existe et que le bot est démarré depuis la racine du projet.

### Les logs sont vides

Le bot vient probablement d'être démarré. Attendez quelques événements ou exécutez des commandes pour générer des logs.

## Support

Pour toute question sur le système de logging :
- Consultez cette documentation
- Vérifiez les logs d'erreur dans l'interface web
- Contactez les administrateurs

---

**Développé pour optimiser les performances et faciliter le débogage du Bot Discord Zone01**

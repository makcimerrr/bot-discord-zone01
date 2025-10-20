# Interface Web du Bot Discord Zone01

## Description

L'interface web est un tableau de bord moderne et intuitif qui permet de visualiser et gérer toutes les informations du bot Discord Zone01. Elle est développée avec Flask et Bootstrap 5.

![Dashboard](https://via.placeholder.com/800x400/002e7a/ffffff?text=Bot+Discord+Zone01+Dashboard)

## Fonctionnalités

### 1. Tableau de Bord (Page d'Accueil)
- **Statistiques en temps réel** :
  - Nombre total de demandes d'aide
  - Demandes d'aide actives
  - Queries configurées
  - Statut du bot

- **Informations principales** :
  - Queries de recherche (Alternances et CDI)
  - Informations du serveur Discord
  - Accès rapide aux différentes sections

- **Actualisation automatique** : Les statistiques sont mises à jour automatiquement toutes les 10 secondes

### 2. Liste des Commandes
- **Visualisation complète** de toutes les commandes du bot
- **Organisation par catégories** :
  - Administration
  - Configuration
  - Utilitaire
  - Événements
  - Système d'Aide

- **Informations détaillées** :
  - Nom de la commande
  - Description
  - Utilisation
  - Alias disponibles
  - Niveau d'accès (Admin/Tous)

### 3. Système d'Aide
- **Statistiques du système** :
  - Demandes en cours
  - Helpers assignés
  - Demandes en attente

- **Liste des demandes actives** :
  - ID de la demande
  - User ID et Guild ID
  - Helper actuel
  - Nombre de helpers contactés
  - Statut de la demande

- **Actualisation automatique** : La liste est actualisée toutes les 30 secondes

- **Explication du fonctionnement** : Guide visuel du processus

### 4. Configuration
- **Variables d'environnement** :
  - QUERY_INTERNSHIP
  - QUERY_FULLTIME
  - DISCORD_TOKEN (masqué pour sécurité)

- **IDs Discord** :
  - Guild ID
  - Canaux (Inter-Promo, Forums)

- **Rôles Discord** :
  - Rôle Helper
  - Rôles des promotions

- **Canaux de progression** : Liste complète des canaux par promotion

## Installation

### Prérequis
- Python 3.8+
- Flask
- Bot Discord Zone01 configuré

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Le fichier `requirements.txt` contient déjà Flask :
```
discord.py
requests
apscheduler
python-dotenv
notion-client
flask
```

## Utilisation

### Démarrage de l'interface web

1. **Depuis la ligne de commande** :
```bash
python web_interface.py
```

2. **Accès à l'interface** :
Ouvrez votre navigateur et accédez à :
```
http://localhost:5000
```

3. **L'interface affichera** :
```
==================================================
Interface Web du Bot Discord Zone01
==================================================
🌐 L'interface web est disponible sur :
   http://localhost:5000
==================================================
```

### Configuration

Par défaut, l'interface web écoute sur :
- **Host** : `0.0.0.0` (accessible depuis le réseau local)
- **Port** : `5000`

Pour modifier ces paramètres, éditez le fichier `web_interface.py` :

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## API REST

L'interface web expose également une API REST pour récupérer des données en temps réel.

### Endpoints disponibles

#### 1. Statistiques
```
GET /api/stats
```

**Réponse** :
```json
{
  "total_help_requests": 5,
  "active_requests": 2,
  "timestamp": "2025-01-20T10:30:00.000000"
}
```

#### 2. Demandes d'aide
```
GET /api/help-requests
```

**Réponse** :
```json
{
  "user_id_message_id": {
    "user_id": 123456789,
    "guild_id": 987654321,
    "contacted_helpers": [111111111, 222222222],
    "current_helper": 222222222
  }
}
```

## Structure des Fichiers

```
bot-discord-zone01/
├── web_interface.py          # Serveur Flask
├── templates/                # Templates HTML
│   ├── base.html            # Template de base
│   ├── index.html           # Page d'accueil
│   ├── commands.html        # Liste des commandes
│   ├── help_system.html     # Système d'aide
│   └── config.html          # Configuration
├── static/                   # Fichiers statiques (CSS, JS, images)
└── data/                     # Données JSON
    ├── config.json          # Configuration Discord
    └── help_requests.json   # Demandes d'aide
```

## Captures d'Écran

### Page d'Accueil
Tableau de bord avec statistiques en temps réel et accès rapide.

### Liste des Commandes
Vue complète de toutes les commandes organisées par catégories.

### Système d'Aide
Suivi des demandes d'aide et des helpers assignés.

### Configuration
Visualisation de toute la configuration du bot.

## Sécurité

- Le token Discord est **masqué** dans l'interface
- Aucune modification n'est possible depuis l'interface (lecture seule)
- L'interface est en **mode debug** par défaut (à désactiver en production)

### Pour la production

Modifiez `web_interface.py` :

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

Et utilisez un serveur WSGI comme Gunicorn :

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_interface:app
```

## Technologies Utilisées

- **Backend** : Flask (Python)
- **Frontend** :
  - Bootstrap 5
  - Bootstrap Icons
  - JavaScript (Vanilla)
- **Design** : Interface moderne avec dégradés et animations

## Support

Pour toute question ou problème :
- Consultez la documentation du bot
- Contactez les administrateurs
- Ouvrez une issue sur GitHub

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

**Développé avec ❤️ pour Zone01 Rouen Normandie**

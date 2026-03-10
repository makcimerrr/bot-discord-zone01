# 🤖 Bot Discord Zone01 - Documentation Complète

## 📋 Table des matières

1. [Introduction](#introduction)
2. [Prérequis](#prérequis)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Lancement du bot](#lancement-du-bot)
6. [Fonctionnalités](#fonctionnalités)
7. [Commandes disponibles](#commandes-disponibles)
8. [Architecture du projet](#architecture-du-projet)
9. [Logs et monitoring](#logs-et-monitoring)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Introduction

Le Bot Discord Zone01 est un bot personnalisé conçu pour gérer et automatiser diverses tâches sur le serveur Discord de Zone01 Rouen Normandie. Il offre des fonctionnalités d'administration, de gestion d'aide entre étudiants, et de suivi automatique des offres d'emploi (alternances et CDI).

### Principales fonctionnalités :
- **Système d'aide automatisé** : Permet aux étudiants de demander de l'aide via un bouton, contacte automatiquement des Helpers disponibles, et enregistre tout l'historique avec statistiques
- **Gestion d'offres d'emploi** : Recherche et publication automatique d'offres d'alternance et de CDI depuis LinkedIn (via API Coresignal)
- **Suivi de progression** : Affichage de la timeline et progression des promotions avec mise à jour en temps réel
- **Configuration dynamique** : Ajout de promotions à la volée avec configuration automatique des canaux et rôles
- **Logging centralisé** : Système de logs détaillé avec différents niveaux et catégories
- **Commandes d'administration** : Gestion des configurations et mises à jour

---

## 💻 Prérequis

Avant d'installer le bot, assurez-vous d'avoir :

- **Python 3.8+** installé sur votre machine
- **pip** (gestionnaire de paquets Python)
- **Git** (optionnel, pour cloner le projet)
- Un **serveur Discord** avec les permissions d'administrateur
- Un **token de bot Discord** (voir section Configuration)
- Une **clé API Coresignal** (pour les fonctionnalités de recherche d'emploi)

---

## 🔧 Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd bot-discord-zone01
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
# Sur macOS/Linux :
source venv/bin/activate

# Sur Windows :
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les dépendances principales sont :
- `discord.py` - Bibliothèque Discord pour Python
- `requests` - Pour les requêtes HTTP
- `apscheduler` - Planification de tâches automatiques
- `python-dotenv` - Gestion des variables d'environnement
- `notion-client` - Intégration avec Notion (optionnel)

---

## ⚙️ Configuration

### 1. Créer une application Discord

1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Cliquez sur "New Application"
3. Donnez un nom à votre application
4. Allez dans l'onglet "Bot"
5. Cliquez sur "Add Bot"
6. **Copiez le TOKEN** (vous en aurez besoin)
7. Activez les intents suivants :
   - Presence Intent
   - Server Members Intent
   - Message Content Intent

### 2. Inviter le bot sur votre serveur

1. Dans le Developer Portal, allez dans "OAuth2" > "URL Generator"
2. Cochez les scopes :
   - `bot`
   - `applications.commands`
3. Cochez les permissions nécessaires :
   - Administrator (ou permissions spécifiques selon vos besoins)
4. Copiez l'URL générée et ouvrez-la dans votre navigateur
5. Sélectionnez votre serveur et autorisez le bot

### 3. Configurer le fichier `.env`

Créez un fichier `.env` à la racine du projet avec le contenu suivant :

```env
# Token Discord (OBLIGATOIRE)
TOKEN='VOTRE_TOKEN_DISCORD_ICI'

# Clés API pour recherche d'emploi
RAPIDAPI_KEY='your_rapidapi_key'
RAPIDAPI_KEY2='your_rapidapi_key2'

# Queries de recherche d'emploi
QUERY_INTERNSHIP='Développeur Web Alternance France'
QUERY_FULLTIME='Développeur Full Stack CDI France'

# Configuration Notion (optionnel)
NOTION_TOKEN='your_notion_token'
NOTION_DATABASE_ID='your_notion_database_id'
```

**⚠️ IMPORTANT** : Ne partagez jamais votre fichier `.env` ou votre token Discord publiquement !

### 4. Configurer le fichier `data/config.json`

Le fichier `data/config.json` contient les IDs des canaux et rôles Discord spécifiques à votre serveur :

```json
{
  "channel_inter_promo": 0,
  "forum_channel_id": 0,
  "forum_channel_id_cdi": 0,
  "role_ping_cdi": 0,
  "role_ping_alternance": 0,
  "guild_id": 0,
  "role_p1_2023": 0,
  "role_p2_2023": 0,
  "role_p1_2024": 0,
  "role_help": 0,
  "channel_progress_P1_2022": 0,
  "channel_progress_P1_2023": 0,
  "channel_progress_P2_2023": 0,
  "channel_progress_P1_2024": 0,
  "channel_progress_P1_2025": 0
}
```

**Comment obtenir les IDs Discord :**

1. Activez le mode développeur dans Discord :
   - Paramètres utilisateur > Avancé > Mode développeur
2. Clic droit sur un canal/rôle/serveur > "Copier l'identifiant"
3. Remplacez les `0` par les IDs copiés

**Configuration minimale requise :**
- `guild_id` : ID de votre serveur Discord
- `role_help` : ID du rôle "Helper" pour le système d'aide

---

## 🚀 Lancement du bot

### Démarrage simple

```bash
python bot.py
```

### Démarrage avec logs détaillés

```bash
python bot.py 2>&1 | tee bot.log
```

### Démarrage en arrière-plan (Linux/macOS)

```bash
nohup python bot.py &
```

### Utilisation avec PM2 (recommandé pour production)

```bash
# Installer PM2
npm install -g pm2

# Démarrer le bot
pm2 start bot.py --name bot-discord-zone01 --interpreter python3

# Voir les logs
pm2 logs bot-discord-zone01

# Redémarrer le bot
pm2 restart bot-discord-zone01

# Arrêter le bot
pm2 stop bot-discord-zone01
```

### Vérification du démarrage

Si le bot démarre correctement, vous devriez voir dans les logs :

```
✓ Bot Discord démarré avec succès
✓ Extension chargée : cogs.administration_cog
✓ Extension chargée : cogs.configuration_cog
✓ Extension chargée : cogs.utilitaire_cog
✓ Extension chargée : cogs.reaction_help_cog
✓ Synchronisation de X commande(s) slash
✓ Scheduler démarré pour les mises à jour automatiques
✓ Bot connecté à Discord
```

---

## 🎨 Fonctionnalités

### 1. Système d'aide automatisé

Le système d'aide permet aux étudiants de demander de l'aide et contacte automatiquement des Helpers disponibles.

**Comment ça marche :**

1. Un admin configure le message d'aide avec `/setup_reaction_help`
2. Un étudiant clique sur le bouton "Demander de l'aide 🆘"
3. Le bot contacte un Helper aléatoire en MP avec les boutons ✅/❌
4. Si le Helper accepte (✅), l'étudiant est mis en relation
5. Si le Helper refuse (❌), un autre Helper est contacté automatiquement

**Fonctionnalités avancées :**
- Évite de contacter plusieurs fois le même Helper pour une même demande
- Gère automatiquement l'indisponibilité des MPs
- Persiste les données entre les redémarrages
- Permet de recharger les boutons après un crash

### 2. Gestion des offres d'emploi

Le bot recherche et publie automatiquement des offres d'emploi depuis LinkedIn via l'API Coresignal.

**Deux types d'offres :**
- **Alternances/Stages** : Basé sur `QUERY_INTERNSHIP`
- **CDI** : Basé sur `QUERY_FULLTIME`

**Mise à jour automatique :**
- 2 fois par jour via le scheduler (configurable dans `utils/scheduler.py`)
- Peut être déclenchée manuellement avec les commandes admin

**Filtrage intelligent :**
- Évite les doublons
- Exclut les mots-clés interdits (configurés dans `data/config.json`)
- Vérifie que les offres sont toujours actives

### 3. Système de logs

Logs centralisés avec plusieurs niveaux :
- 🔵 `INFO` : Informations générales
- ✅ `SUCCESS` : Opérations réussies
- ⚠️ `WARNING` : Avertissements
- ❌ `ERROR` : Erreurs

Catégories de logs :
- `bot` : Événements du bot principal
- `help_system` : Système d'aide
- `jobs` : Recherche d'offres d'emploi
- `scheduler` : Tâches planifiées

Les logs sont stockés dans `data/bot_logs.json` et peuvent être consultés en temps réel.

### 4. Suivi de progression

Affiche la timeline et la progression des différentes promotions sur le parcours Zone01.

### 5. Gestion de la configuration

Le bot permet de gérer facilement la configuration via des commandes slash.

**Fonctionnalités :**
- **Affichage de la config** : Visualise tous les IDs configurés avec leurs noms
- **Modification en ligne** : Change les IDs de canaux et rôles sans éditer manuellement `config.json`
- **Validation automatique** : Vérifie que les IDs correspondent à des canaux/rôles existants
- **Logs des modifications** : Toutes les modifications sont enregistrées

**Utilisation :**

1. Pour voir la configuration actuelle :
   ```
   /show_config
   ```
   Affiche un embed avec :
   - Informations du serveur
   - Liste des canaux configurés (avec mentions)
   - Liste des rôles configurés (avec mentions)

2. Pour modifier un ID :
   ```
   /edit_config key: [sélection] value: [ID ou mention]
   ```
   - Sélectionner la clé dans la liste déroulante
   - Entrer la valeur de 3 façons possibles :
     - **Mention de canal** : `#general` (Discord auto-complète)
     - **Mention de rôle** : `@Helper` (Discord auto-complète)
     - **ID direct** : `1234567890123456789`
   - Le bot extrait automatiquement l'ID depuis la mention
   - Valide et confirme la modification
   - Affiche si le canal/rôle a été trouvé

**Avantages :**
- Plus besoin d'éditer manuellement `config.json`
- **Support des mentions @ et #** (plus facile et rapide)
- Discord auto-complète les mentions
- Validation immédiate des IDs
- Historique des modifications dans les logs
- Interface intuitive avec sélection par menu

---

## 🎮 Commandes disponibles

### Commandes Slash (/)

#### Système d'aide

| Commande | Description | Paramètres | Admin |
|----------|-------------|------------|-------|
| `/setup_reaction_help` | Configure le message d'aide avec bouton | `channel` | ✅ |
| `/reload_help_message` | Recharge le message d'aide (supprime l'ancien) | `channel` | ✅ |
| `/help_logs` | ✨ Affiche l'historique des demandes avec statistiques | `limit` (optionnel, défaut: 20) | ✅ |

#### Configuration

| Commande | Description | Paramètres | Admin |
|----------|-------------|------------|-------|
| `/show_config` | Affiche la configuration avec toutes les promotions | Aucun | ✅ |
| `/edit_config` | Édite la configuration (IDs canaux/rôles) | `key`, `value` | ✅ |
| `/add_promotion` | ✨ Ajoute une nouvelle promotion dynamiquement | `promotion_name`, `channel`, `role` | ✅ |

#### Progression

| Commande | Description | Paramètres | Admin |
|----------|-------------|------------|-------|
| `/timeline` | ✨ Met à jour la progression avec suivi en temps réel | Aucun | ✅ |

#### Utilitaire

Les commandes utilitaires utilisent le préfixe `!` :

| Commande | Description | Aliases | Admin |
|----------|-------------|---------|-------|
| `!ping` | Affiche la latence du bot | `pingme`, `pingpong`, `pingtest` | ❌ |
| `!help` | Affiche l'aide des commandes | `helpme` | ❌ |

#### Administration (préfixe !)

| Commande | Description | Admin |
|----------|-------------|-------|
| `!setqueryIntern <query>` | Définit la query de recherche pour les alternances | ✅ |
| `!setqueryFulltime <query>` | Définit la query de recherche pour les CDI | ✅ |
| `!showqueryIntern` | Affiche la query actuelle pour les alternances | ✅ |
| `!showqueryFulltime` | Affiche la query actuelle pour les CDI | ✅ |
| `!update_internships` | Force la mise à jour des offres d'alternance | ✅ |
| `!update_fulltime` | Force la mise à jour des offres de CDI | ✅ |
| `!timeline` | Affiche la timeline des promotions | ✅ |

### Exemples d'utilisation

```
# Configurer le système d'aide
/setup_reaction_help channel: #aide

# Recharger le message d'aide après un redémarrage
/reload_help_message channel: #aide

# ✨ Consulter l'historique des demandes d'aide (30 derniers événements)
/help_logs limit: 30

# Afficher la configuration du bot
/show_config

# ✨ Ajouter une nouvelle promotion
/add_promotion promotion_name: P2 2025 channel: #progression-p2-2025 role: @P2 2025

# Modifier la configuration avec une mention de canal
/edit_config key: Forum Alternances value: #alternances

# Modifier la configuration avec une mention de rôle
/edit_config key: Rôle Helper value: @Helper

# Ou utiliser un ID direct
/edit_config key: ID du Serveur value: 1234567890123456789

# ✨ Mettre à jour la progression avec suivi en temps réel
/timeline

# Vérifier la latence du bot
!ping

# Définir une nouvelle recherche d'alternance
!setqueryIntern Développeur Python Alternance Normandie

# Forcer la mise à jour des offres
!update_internships

# Version classique de timeline (sans suivi)
!timeline
```

---

## 📁 Architecture du projet

```
bot-discord-zone01/
├── bot.py                          # Point d'entrée principal
├── requirements.txt                # Dépendances Python
├── .env                           # Variables d'environnement (à créer)
├── DOCUMENTATION.md               # Cette documentation
├── README.md                      # Readme du projet
│
├── cogs/                          # Extensions du bot (modules)
│   ├── __init__.py
│   ├── administration_cog.py      # Commandes admin
│   ├── configuration_cog.py       # Configuration et affichage
│   ├── reaction_help_cog.py       # Système d'aide avec boutons
│   └── utilitaire_cog.py         # Commandes utilitaires (ping, etc.)
│
├── utils/                         # Utilitaires et helpers
│   ├── __init__.py
│   ├── config_loader.py          # Chargement de la config
│   ├── logger.py                 # Système de logging
│   ├── scheduler.py              # Planificateur de tâches
│   ├── handlers.py               # Gestionnaires d'événements
│   ├── utils_function.py         # Fonctions utilitaires
│   ├── utils_internship.py       # Gestion des alternances
│   ├── utils_fulltime.py         # Gestion des CDI
│   ├── utils_departement.py      # Utilitaires de département
│   ├── intern_fetcher.py         # Récupération offres alternance
│   ├── cdi_fetcher.py            # Récupération offres CDI
│   ├── progress_fetcher.py       # Récupération progression
│   ├── timeline.py               # Timeline des promotions
│   ├── notifier.py               # Système de notifications
│   └── models.py                 # Modèles de données
│
└── data/                          # Données persistantes
    ├── config.json                # Configuration (IDs Discord)
    ├── bot_logs.json              # Logs du bot
    ├── help_requests.json         # Demandes d'aide en cours
    └── technologies.json          # Liste des technologies
```

### Description des composants

#### `bot.py`
Point d'entrée principal du bot. Gère :
- L'initialisation du bot Discord
- Le chargement des extensions (cogs)
- La synchronisation des commandes slash
- Les événements globaux (on_ready, on_error, etc.)
- Le démarrage du scheduler

#### `cogs/` (Extensions)
Les cogs sont des modules qui étendent les fonctionnalités du bot :

- **administration_cog.py** : Commandes administrateur
  - Gestion des queries de recherche d'emploi
  - Mise à jour manuelle des offres
  - Timeline des promotions

- **configuration_cog.py** : Affichage de la configuration
  - Affiche les queries actuelles
  - Affiche la configuration du bot

- **reaction_help_cog.py** : Système d'aide
  - Vue avec bouton pour demander de l'aide
  - Gestion des demandes d'aide
  - Contact automatique des Helpers
  - Gestion des réponses des Helpers

- **utilitaire_cog.py** : Commandes utilitaires
  - Commande ping pour tester la latence
  - Autres commandes utilitaires

#### `utils/` (Utilitaires)
Fonctions et classes réutilisables :

- **config_loader.py** : Charge la config depuis `.env` et `config.json`
- **logger.py** : Système de logging avec niveaux et catégories
- **scheduler.py** : Configure les tâches automatiques (APScheduler)
- **handlers.py** : Gestionnaires d'événements (DM, etc.)
- **utils_function.py** : Fonctions utilitaires génériques
- **utils_internship.py** : Logique métier pour les alternances
- **utils_fulltime.py** : Logique métier pour les CDI
- **intern_fetcher.py** : Récupère les offres d'alternance depuis l'API
- **cdi_fetcher.py** : Récupère les offres de CDI depuis l'API
- **timeline.py** : Gère l'affichage de la timeline

#### `data/` (Données)
Fichiers de données persistantes :

- **config.json** : Configuration serveur (IDs Discord)
- **bot_logs.json** : Logs du bot (max 1000 entrées)
- **help_requests.json** : État des demandes d'aide en cours
- **technologies.json** : Liste des technologies pour filtrage

---

## 📊 Logs et monitoring

### Système de logs

Le bot utilise un système de logging personnalisé défini dans `utils/logger.py`.

**Niveaux de logs :**
```python
logger.info("Message d'information", category="bot")
logger.success("Opération réussie", category="bot")
logger.warning("Avertissement", category="bot")
logger.error("Erreur critique", category="bot")
```

**Catégories de logs :**
- `bot` : Événements du bot principal
- `help_system` : Système d'aide
- `jobs` : Recherche d'offres d'emploi
- `scheduler` : Tâches planifiées
- `web` : Interface web (si utilisée)

### Consulter les logs

Les logs sont stockés dans `data/bot_logs.json` et affichés dans le terminal lors de l'exécution.

**Format des logs :**
```json
{
  "timestamp": "2025-01-21T10:30:45.123456",
  "level": "INFO",
  "category": "bot",
  "message": "Bot démarré avec succès"
}
```

### Statistiques

Le système de logs fournit des statistiques :
- Nombre total de logs
- Répartition par niveau (INFO, SUCCESS, WARNING, ERROR)
- Répartition par catégorie

---

## 🔧 Troubleshooting

### Le bot ne démarre pas

**Problème : `discord.errors.LoginFailure: Improper token has been passed`**
- Vérifiez que votre token dans `.env` est correct
- Assurez-vous qu'il n'y a pas d'espaces avant/après le token
- Régénérez un nouveau token sur le Discord Developer Portal

**Problème : `ModuleNotFoundError`**
- Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`
- Assurez-vous d'être dans l'environnement virtuel si vous en utilisez un

**Problème : `FileNotFoundError: .env file not found`**
- Créez le fichier `.env` à la racine du projet
- Copiez le template fourni dans la section Configuration

### Les commandes slash ne s'affichent pas

1. Vérifiez que les commandes ont été synchronisées (message dans les logs)
2. Attendez quelques minutes (la synchronisation peut prendre du temps)
3. Essayez de relancer le bot
4. Vérifiez que le bot a bien les permissions `applications.commands`

### Le système d'aide ne fonctionne pas

**Problème : Le bouton ne répond pas**
- Vérifiez que le bot est en ligne
- Rechargez le message avec `/reload_help_message`
- Vérifiez les logs pour voir s'il y a des erreurs

**Problème : Les Helpers ne reçoivent pas de MP**
- Vérifiez que le rôle Helper (`role_help`) est correctement configuré dans `config.json`
- Assurez-vous que les Helpers acceptent les MPs des membres du serveur
- Vérifiez les logs pour voir si le bot a tenté d'envoyer les MPs

**Problème : Les boutons ✅/❌ dans les MPs ne fonctionnent pas**
- Le bot utilise des vues persistantes, rechargez le message avec `/reload_help_message`
- Vérifiez que le bot est en ligne quand le Helper clique sur le bouton

### Les offres d'emploi ne sont pas publiées

**Problème : Pas de nouvelles offres**
- Vérifiez que `RAPIDAPI_KEY` est configuré dans `.env`
- Vérifiez que les queries (`QUERY_INTERNSHIP`, `QUERY_FULLTIME`) sont définies
- Vérifiez que les IDs de canaux forum sont corrects dans `config.json`
- Consultez les logs pour voir s'il y a des erreurs API

**Problème : Erreur API Coresignal**
- Vérifiez que votre clé API est valide et non expirée
- Vérifiez que vous n'avez pas dépassé votre quota d'API

### Erreurs de permissions

**Problème : `discord.errors.Forbidden`**
- Vérifiez que le bot a les permissions nécessaires sur le serveur
- Pour les canaux forum : permission de créer des posts
- Pour les canaux texte : permission de lire, envoyer des messages, ajouter des réactions
- Pour les MPs : le bot doit pouvoir envoyer des MPs (géré par les paramètres utilisateur)

### Le bot se déconnecte souvent

**Problème : Déconnexions fréquentes**
- Vérifiez votre connexion internet
- Vérifiez les logs Discord pour voir s'il y a des problèmes de service
- Utilisez un hébergeur stable pour la production (VPS, cloud, etc.)
- Envisagez d'utiliser PM2 pour redémarrer automatiquement le bot

### Logs non visibles

**Problème : Les logs ne s'affichent pas dans le terminal**
- Vérifiez que le niveau de log n'est pas trop restrictif
- Assurez-vous que le fichier `data/bot_logs.json` est accessible en écriture
- Vérifiez les permissions du dossier `data/`

---

## 🔐 Sécurité

### Bonnes pratiques

1. **Ne jamais commit le fichier `.env`** dans Git
   - Le `.env` contient des informations sensibles (token, clés API)
   - Utilisez `.gitignore` pour exclure `.env`

2. **Régénérer les tokens compromis**
   - Si vous partagez accidentellement votre token, régénérez-le immédiatement
   - Allez sur Discord Developer Portal > Bot > Reset Token

3. **Limiter les permissions du bot**
   - Ne donnez que les permissions nécessaires
   - Évitez "Administrator" en production si possible

4. **Sécuriser l'hébergement**
   - Utilisez un serveur sécurisé (firewall, SSH key, etc.)
   - Mettez à jour régulièrement les dépendances

5. **Valider les entrées utilisateur**
   - Le bot valide déjà les queries de recherche
   - Ajoutez des validations supplémentaires si nécessaire

---

## 🚀 Déploiement en production

### Option 1 : VPS (Linux)

```bash
# Se connecter au VPS
ssh user@your-vps-ip

# Cloner le projet
git clone <url-du-repo>
cd bot-discord-zone01

# Installer Python et pip
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer .env et config.json
nano .env
nano data/config.json

# Installer PM2
sudo npm install -g pm2

# Démarrer le bot avec PM2
pm2 start bot.py --name bot-discord-zone01 --interpreter python3

# Configurer PM2 pour démarrer au boot
pm2 startup
pm2 save

# Voir les logs
pm2 logs bot-discord-zone01
```

### Option 2 : Docker

Créez un `Dockerfile` :

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY bot.py .
COPY cogs ./cogs
COPY utils ./utils
COPY data ./data
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv
COPY .env .
CMD ["python", "bot.py"]
```

Créez un `docker-compose.yml` :

```yaml
version: '3.8'
services:
  bot:
    build: .
    container_name: discord_bot
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    command: python bot.py
```

Démarrer avec Docker :

```bash
docker compose build
docker compose up -d
docker compose logs --tail=30
```

### Option 3 : Service systemd (Linux)

Créez `/etc/systemd/system/bot-discord.service` :

```ini
[Unit]
Description=Bot Discord Zone01
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/bot-discord-zone01
ExecStart=/path/to/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activer et démarrer :

```bash
sudo systemctl daemon-reload
sudo systemctl enable bot-discord
sudo systemctl start bot-discord
sudo systemctl status bot-discord
```

---

## 📝 Maintenance

### Mise à jour du bot

```bash
# Sauvegarder les données
cp -r data/ data_backup/

# Récupérer les dernières modifications
git pull

# Mettre à jour les dépendances
pip install --upgrade -r requirements.txt

# Redémarrer le bot
pm2 restart bot-discord-zone01
```

### Nettoyage des logs

Les logs sont automatiquement limités à 1000 entrées. Pour nettoyer manuellement :

```python
# Dans Python
from utils.logger import logger
logger.clear_logs()
```

### Sauvegarde

Fichiers à sauvegarder régulièrement :
- `data/config.json`
- `data/help_requests.json`
- `.env` (en sécurité)

```bash
# Script de sauvegarde
tar -czf backup-$(date +%Y%m%d).tar.gz data/ .env
```

---

## 🤝 Contribution

Pour contribuer au projet :

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📞 Support

Pour toute question ou problème :

- Consultez cette documentation
- Vérifiez les logs du bot
- Consultez la section Troubleshooting
- Ouvrez une issue sur le dépôt Git

---

## 📜 Licence

Ce projet est destiné à un usage interne pour Zone01 Rouen Normandie.

---

## 🙏 Remerciements

- Discord.py pour la bibliothèque Discord
- Coresignal pour l'API de recherche d'offres d'emploi LinkedIn
- La communauté Zone01 Rouen Normandie

---

**Dernière mise à jour : Janvier 2025**

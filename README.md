# 🤖 Bot Discord Zone01

Bot Discord automatisé pour gérer et faciliter les interactions sur le serveur Discord de Zone01 Rouen Normandie.

## 🚀 Démarrage rapide

### Installation

```bash
# Cloner le projet
git clone <url-du-repo>
cd bot-discord-zone01

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos tokens et clés API

# Lancer le bot
python bot.py
```

### Configuration minimale

1. **Créer un bot Discord** sur [Discord Developer Portal](https://discord.com/developers/applications)
2. **Récupérer le token** et le mettre dans `.env`
3. **Configurer `data/config.json`** avec les IDs de votre serveur Discord
4. **Lancer le bot** avec `python bot.py`

## 📚 Fonctionnalités principales

### 🆘 Système d'aide automatisé
- Les étudiants peuvent demander de l'aide via un bouton
- Le bot contacte automatiquement des Helpers disponibles
- Gestion intelligente des refus et acceptations
- **Nouveau** : Historique complet des demandes avec statistiques

### 💼 Gestion d'offres d'emploi
- Recherche automatique d'offres d'alternance et CDI sur LinkedIn
- Publication automatique dans des canaux forum
- Mise à jour 2x par jour via scheduler

### 📊 Suivi de progression
- Affichage de la timeline des promotions avec suivi en temps réel
- Suivi de la progression des étudiants
- **Nouveau** : Mise à jour interactive avec barre de progression

### ⚙️ Configuration dynamique
- **Nouveau** : Ajout de promotions à la volée avec `/add_promotion`
- Configuration automatique des canaux et rôles pour chaque promotion
- Affichage dynamique de toutes les promotions configurées

### 📝 Système de logging
- Logs détaillés avec niveaux (INFO, SUCCESS, WARNING, ERROR)
- Catégorisation par système (bot, help_system, jobs, scheduler)
- Stockage persistant dans `data/bot_logs.json`
- **Nouveau** : Logs dédiés pour le système d'aide avec statistiques

## 🎮 Commandes principales

### Commandes Slash

#### Configuration
- `/show_config` - Affiche la configuration du bot avec toutes les promotions
- `/edit_config` - Modifie la configuration (canaux/rôles)
- **`/add_promotion`** - Ajoute une nouvelle promotion avec son canal et rôle ✨

#### Système d'aide
- `/setup_reaction_help` - Configure le message d'aide avec bouton
- `/reload_help_message` - Recharge le message d'aide
- **`/help_logs`** - Affiche l'historique et les statistiques du système d'aide ✨

#### Progression
- **`/timeline`** - Met à jour la progression avec suivi en temps réel ✨

### Commandes Prefix (!)
- `!ping` - Test de latence
- `!help` - Affiche l'aide
- `!setqueryIntern <query>` - Définit la recherche d'alternance (admin)
- `!setqueryFulltime <query>` - Définit la recherche de CDI (admin)
- `!update_internships` - Force la mise à jour des alternances (admin)
- `!update_fulltime` - Force la mise à jour des CDI (admin)
- `!timeline` - Affiche la timeline des promotions (admin) - _Version classique_

## 📁 Structure du projet

```
bot-discord-zone01/
├── bot.py                      # Point d'entrée
├── requirements.txt            # Dépendances
├── .env                        # Configuration (à créer)
├── README.md                   # Ce fichier
├── DOCUMENTATION.md            # Documentation complète
├── cogs/                       # Extensions du bot
│   ├── administration_cog.py
│   ├── configuration_cog.py
│   ├── reaction_help_cog.py
│   └── utilitaire_cog.py
├── utils/                      # Utilitaires
│   ├── config_loader.py
│   ├── logger.py
│   ├── scheduler.py
│   ├── handlers.py
│   └── ...
└── data/                       # Données persistantes
    ├── config.json             # Configuration du bot
    ├── bot_logs.json           # Logs généraux
    ├── help_requests.json      # Demandes d'aide en cours
    ├── help_logs.json          # Historique des demandes d'aide
    └── technologies.json       # Technologies pour les offres
```

## 🔧 Configuration

### Variables d'environnement (`.env`)

```env
TOKEN='votre_token_discord'
RAPIDAPI_KEY='votre_cle_rapidapi'
QUERY_INTERNSHIP='Développeur Web Alternance France'
QUERY_FULLTIME='Développeur Full Stack CDI France'
NOTION_TOKEN='votre_token_notion'
NOTION_DATABASE_ID='votre_database_id'
```

### Configuration Discord (`data/config.json`)

Contient les IDs de canaux, rôles et serveur. Voir `DOCUMENTATION.md` pour plus de détails.

## 📖 Documentation complète

Pour une documentation complète incluant :
- Installation détaillée
- Configuration avancée
- Toutes les commandes
- Architecture du projet
- Troubleshooting
- Déploiement en production

👉 **Consultez [DOCUMENTATION.md](DOCUMENTATION.md)**

## 🛠️ Technologies utilisées

- **Discord.py** - Bibliothèque Discord pour Python
- **APScheduler** - Planification de tâches automatiques
- **Requests** - Requêtes HTTP
- **python-dotenv** - Gestion des variables d'environnement
- **Notion Client** - Intégration Notion (optionnel)

## 🔐 Sécurité

⚠️ **Important** :
- Ne jamais commit le fichier `.env`
- Ne jamais partager votre token Discord
- Régénérer immédiatement tout token compromis

## 🐛 Troubleshooting

### Le bot ne démarre pas
- Vérifiez que le token dans `.env` est correct
- Vérifiez que toutes les dépendances sont installées

### Les commandes slash ne s'affichent pas
- Attendez quelques minutes (synchronisation)
- Relancez le bot
- Vérifiez que le bot a les permissions `applications.commands`

### Le système d'aide ne fonctionne pas
- Rechargez le message avec `/reload_help_message`
- Vérifiez que `role_help` est configuré dans `config.json`
- Consultez les logs pour identifier les erreurs

Pour plus de solutions, consultez la section Troubleshooting de `DOCUMENTATION.md`.

## 📊 Logs

Les logs sont stockés dans `data/bot_logs.json` et affichés en temps réel dans le terminal.

Niveaux de logs :
- 🔵 `INFO` - Informations générales
- ✅ `SUCCESS` - Opérations réussies
- ⚠️ `WARNING` - Avertissements
- ❌ `ERROR` - Erreurs

## 🚀 Déploiement

### Avec PM2 (recommandé)
```bash
pm2 start bot.py --name bot-discord-zone01 --interpreter python3
pm2 save
pm2 startup
```

### Avec Docker
```bash
docker-compose up -d
```

Voir `DOCUMENTATION.md` pour plus d'options de déploiement.

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez `DOCUMENTATION.md` pour les guidelines.

## Convention Release

En suivant les conventions de versionnement sémantique (SemVer) :

- **MAJOR**: version (X.y.z) pour les changements incompatibles de l'API
- **MINOR**: version (x.Y.z) pour les ajouts de fonctionnalités rétrocompatibles
- **PATCH**: version (x.y.Z) pour les corrections de bugs rétrocompatibles

## 👥 Auteurs

Ce bot a été créé par [Maxime Dubois](https://makcimerrr.com) pour [Zone01 Rouen](https://zone01rouennormandie.org).

## 📜 Licence

Ce projet est sous licence MIT. Pour plus de détails, consultez le fichier [LICENSE](https://github.com/makcimerrr/bot-discord-zone01/blob/main/LICENSE).

## 📞 Support

- Consultez `DOCUMENTATION.md`
- Vérifiez les logs du bot
- Ouvrez une issue sur le dépôt

---

**Développé avec ❤️ pour Zone01 Rouen Normandie**

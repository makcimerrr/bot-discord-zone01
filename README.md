# 🤖 Bot d'Aide pour Apprenants

Ce bot Discord est conçu pour aider à la gestion des offres d'emploi et à la coordination des demandes d'aide au sein d'un serveur Discord spécifique.

## Fonctionnalités

- **Mise à jour des Offres d'Emploi :** Le bot récupère automatiquement les offres d'emploi depuis plusieurs sources (LinkedIn, Indeed, et une API personnalisée) et les publie dans un canal dédié.
- **Gestion des Demandes d'Aide :** Les utilisateurs peuvent signaler qu'ils ont besoin d'aide en réagissant à un message spécifique. Le bot leur attribue un rôle et modifie leur pseudo pour indiquer qu'ils ont besoin d'aide.
- **Système d'Aide par Réaction :** Un système avancé de gestion des demandes d'aide avec contact automatique des Helpers et rotation en cas de refus.
- **Planification Automatique :** Les offres d'emploi sont mises à jour deux fois par jour (matin et soir) grâce à un scheduler intégré.
- **Interface Web :** Tableau de bord moderne pour visualiser toutes les informations du bot, les commandes, et le système d'aide.

## Configuration

Pour utiliser ce bot, vous devez :
1. Avoir Python 3.7+ installé.
2. Installer les dépendances nécessaires via `pip install -r requirements.txt`.
3. Définir les variables d'environnement requises, notamment le TOKEN Discord.
4. Éditer les id des channels et rôles, dans config.json, pour l'envoie et le ping des messages.

## Variables d'Environnement

- `TOKEN`: Token d'authentification de votre bot Discord.
- `RAPID KEY`: Token pour l'accès aux API de [rapid](https://rapidapi.com/)

## Utilisation

### Démarrer le Bot Discord

Pour démarrer le bot, exécutez le fichier Python `bot.py`. Assurez-vous que votre bot a les autorisations nécessaires sur votre serveur Discord pour modifier les pseudonymes et gérer les rôles.

```bash
python bot.py
```

### Démarrer l'Interface Web

L'interface web vous permet de visualiser toutes les informations du bot en temps réel.

```bash
python web_interface.py
```

Ensuite, ouvrez votre navigateur et accédez à : `http://localhost:5000`

**Fonctionnalités de l'interface web :**
- Tableau de bord avec statistiques en temps réel
- Liste complète de toutes les commandes
- Suivi des demandes d'aide actives
- Visualisation de la configuration
- **Logs en temps réel** avec filtrage avancé
- API REST pour récupérer des données

📖 **Documentation complète** : [docs/web_interface.md](docs/web_interface.md)

### Système de Logging

Le bot utilise un système de logging centralisé qui **évite les logs dans le terminal** pour optimiser les performances. Tous les logs sont disponibles dans l'interface web.

- ✅ Aucun log dans le terminal (performance optimale)
- ✅ Interface web moderne pour consulter les logs
- ✅ Filtrage par niveau (INFO, SUCCESS, WARNING, ERROR, DEBUG)
- ✅ Filtrage par catégorie (bot, cog, help_system, etc.)
- ✅ Statistiques en temps réel
- ✅ API REST pour récupérer les logs

📖 **Documentation du système de logging** : [docs/logging_system.md](docs/logging_system.md)

## Contribuer

Si vous souhaitez contribuer à ce projet, vous pouvez :

- Soumettre des suggestions d'amélioration via les issues.
- Proposer des pull requests pour résoudre des problèmes ou ajouter des fonctionnalités.

## Documentation du BOT

[Par ici](https://makcimerrr.github.io/bot-discord-zone01/guide/commandes/)

## Convention Release

En suivant les conventions de versionnement sémantique (SemVer), voici comment cela fonctionne :

- **MAJOR**: version (X.y.z) pour les changements incompatibles de l'API.
- **MINOR**: version (x.Y.z) pour les ajouts de fonctionnalités dans une manière rétrocompatible.
- **PATCH**: version (x.y.Z) pour les corrections de bugs rétrocompatibles.


## Auteurs

Ce bot a été créé par [Maxime Dubois](https://makcimerrr.com) pour [Zone01 Rouen](https://zone01rouennormandie.org).

## Licence

Ce projet est sous licence MIT. Pour plus de détails, consultez le fichier [LICENSE](https://github.com/makcimerrr/bot-discord-zone01/blob/main/LICENSE).

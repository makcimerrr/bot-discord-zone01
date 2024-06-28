# Bot d'Aide pour Apprenants

Ce bot Discord est conçu pour aider à la gestion des offres d'emploi et à la coordination des demandes d'aide au sein d'un serveur Discord spécifique.

## Fonctionnalités

- **Mise à jour des Offres d'Emploi :** Le bot récupère automatiquement les offres d'emploi depuis plusieurs sources (LinkedIn, Indeed, et une API personnalisée) et les publie dans un canal dédié.
- **Gestion des Demandes d'Aide :** Les utilisateurs peuvent signaler qu'ils ont besoin d'aide en réagissant à un message spécifique. Le bot leur attribue un rôle et modifie leur pseudo pour indiquer qu'ils ont besoin d'aide.
- **Planification Automatique :** Les offres d'emploi sont mises à jour deux fois par jour (matin et soir) grâce à un scheduler intégré.

## Configuration

Pour utiliser ce bot, vous devez :
1. Avoir Python 3.7+ installé.
2. Installer les dépendances nécessaires via `pip install -r requirements.txt`.
3. Définir les variables d'environnement requises, notamment le TOKEN Discord.

## Variables d'Environnement

- `TOKEN`: Token d'authentification de votre bot Discord.

## Utilisation

Pour démarrer le bot, exécutez le fichier Python `bot.py`. Assurez-vous que votre bot a les autorisations nécessaires sur votre serveur Discord pour modifier les pseudonymes et gérer les rôles.

## Contribuer

Si vous souhaitez contribuer à ce projet, vous pouvez :

- Soumettre des suggestions d'amélioration via les issues.
- Proposer des pull requests pour résoudre des problèmes ou ajouter des fonctionnalités.

## Auteurs

Ce bot a été créé par [Votre Nom] pour [Nom du Serveur Discord].

## Licence

Ce projet est sous licence MIT. Pour plus de détails, consultez le fichier LICENSE.

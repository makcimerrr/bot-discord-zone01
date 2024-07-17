# Introduction

Ce document explique comment installer et configurer le Bot Discord Zone01.

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

Pour démarrer le bot, exécutez le fichier Python `bot.py`. Assurez-vous que votre bot a les autorisations nécessaires sur votre serveur Discord pour modifier les pseudonymes et gérer les rôles.

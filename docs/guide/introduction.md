# 🛠️ Introduction

Ce document vous guide à travers le processus d'installation et de configuration du **Bot Discord Zone01**. Suivez ces étapes pour mettre en place le bot et le préparer pour une utilisation efficace.

## ⚙️ Configuration

Pour utiliser ce bot, vous devez :

1. **Installer Python 3.7+** 🐍
   - Assurez-vous d'avoir Python version 3.7 ou supérieure installé sur votre machine.

2. **Installer les dépendances** 📦
   - Exécutez la commande suivante pour installer toutes les dépendances nécessaires :
     ```bash
     pip install -r requirements.txt
     ```

3. **Définir les variables d'environnement** 🌍
   - Configurez les variables d'environnement nécessaires, y compris le `TOKEN` Discord. Ces variables permettent au bot de se connecter à Discord et d'interagir avec votre serveur.

4. **Éditer les ID des channels et rôles** ✏️
   - Modifiez le fichier `config.json` pour définir les ID des channels et rôles. Cela permet au bot d'envoyer des messages et de pinguer les bons utilisateurs.

## 🔑 Variables d'Environnement

- **`TOKEN`** : Token d'authentification de votre bot Discord. Il est nécessaire pour que le bot se connecte à l'API Discord.
- **`RAPID KEY`** : Token pour accéder aux API de [RapidAPI](https://rapidapi.com/). Permet au bot d'obtenir des données depuis des services tiers.

## 🚀 Utilisation

Pour démarrer le bot :

1. Exécutez le fichier Python `bot.py` :
   ```bash
   python bot.py

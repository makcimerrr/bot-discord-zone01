# Utilise une image officielle Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY bot.py .
COPY cogs ./cogs
COPY utils ./utils
COPY data ./data

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Installer python-dotenv pour la gestion du .env
RUN pip install python-dotenv

# Copier le fichier .env
COPY .env .

# Commande pour lancer le bot
CMD ["python", "bot.py"]


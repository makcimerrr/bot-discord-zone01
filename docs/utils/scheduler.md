# Documentation pour la gestion des tâches programmées avec `AsyncIOScheduler`, le module scheduler.py

## Description

Ce module utilise `AsyncIOScheduler` de la bibliothèque `APScheduler` pour planifier des tâches asynchrones liées à la mise à jour des listes d'emplois et de CDI. Les tâches sont planifiées pour s'exécuter à des heures spécifiques chaque jour, en utilisant des fonctions définies pour envoyer des mises à jour des listes.

## Importations

- **`AsyncIOScheduler`** : Un planificateur de tâches asynchrone qui fonctionne avec la boucle d'événements `asyncio`.
- **`JobCog`** et **`CDICog`** : Cogs définis dans les modules `cogs.gestion_jobs` et `cogs.gestion_cdi` respectivement, utilisés pour envoyer des listes d'emplois et de CDI.

## Fonctionnalités

### Fonctions de mise à jour

1. **`joblist_morning(bot)`** :
   - Instancie un objet `JobCog` avec le bot.
   - Appelle la méthode `send_joblist()` pour envoyer la liste des emplois.
   - Imprime un message indiquant que la liste des emplois a été mise à jour pour la matinée.

2. **`joblist_evening(bot)`** :
   - Instancie un objet `JobCog` avec le bot.
   - Appelle la méthode `send_joblist()` pour envoyer la liste des emplois.
   - Imprime un message indiquant que la liste des emplois a été mise à jour pour le soir.

3. **`cdi_morning(bot)`** :
   - Instancie un objet `CDICog` avec le bot.
   - Appelle la méthode `send_cdilist()` pour envoyer la liste des CDI.
   - Imprime un message indiquant que la liste des CDI a été mise à jour pour la matinée.

4. **`cdi_evening(bot)`** :
   - Instancie un objet `CDICog` avec le bot.
   - Appelle la méthode `send_cdilist()` pour envoyer la liste des CDI.
   - Imprime un message indiquant que la liste des CDI a été mise à jour pour le soir.

### Fonction de démarrage du planificateur

**`start_scheduler(bot)`** :
   - Configure les tâches programmées pour le bot.
   - Utilise des tâches cron pour exécuter les mises à jour :
     - **Matin** : À 9h00, appelle `joblist_morning(bot)` et `cdi_morning(bot)`.
     - **Soir** : À 18h00, appelle `joblist_evening(bot)` et `cdi_evening(bot)`.
   - Démarre le planificateur avec `scheduler.start()`.

## Exemples d'utilisation

```python
# Supposons que `bot` soit une instance de votre bot Discord
start_scheduler(bot)
```

## Gestion des erreurs

- Les erreurs potentielles liées aux appels de méthodes `send_joblist()` et `send_cdilist()` doivent être gérées dans les définitions de ces méthodes. Les exceptions levées par ces appels seront capturées et traitées par les fonctions appelantes.

## Remarques

- **APScheduler** :
  - Assurez-vous que `APScheduler` est correctement installé et configuré dans votre environnement. La configuration est nécessaire pour utiliser `AsyncIOScheduler` et les tâches cron.
  
- **Cogs** :
  - Assurez-vous que les cogs `JobCog` et `CDICog` sont correctement définis et importés. Les méthodes `send_joblist()` et `send_cdilist()` doivent être correctement implémentées dans ces cogs.

- **Bot** :
  - Le paramètre `bot` passé aux fonctions doit être une instance valide de votre bot Discord, qui est utilisé pour interagir avec l'API Discord.


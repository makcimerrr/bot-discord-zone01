
# Module de Gestion de la commande `!help`

Ce module, intégré au bot Discord Zone01, est responsable de la gestion de la commande `!help`. Cette commande permet aux utilisateurs d'obtenir une liste des commandes disponibles ainsi que des descriptions détaillées de chacune d'entre elles.

## Fonctionnalités

### Commande `!help`
- **Description** : Affiche une liste de toutes les commandes disponibles avec une brève description de chacune.
- **Utilisation** : `!help` ou `!help [commande]`
- **Paramètres** :
  - `[commande]` (optionnel) : Si spécifié, affiche des informations détaillées sur la commande donnée.

### Exemple d'Utilisation
- **Commande** : `!help`
- **Résultat** : Une liste de toutes les commandes disponibles est affichée avec leurs descriptions.

### Exemple d'Utilisation Avancée
- **Commande** : `!help update_jobs`
- **Résultat** : Affiche des informations détaillées sur la commande `update_jobs`, y compris les paramètres et exemples d'utilisation.

### Notes
- La commande `!help` est accessible à tous les utilisateurs du serveur.
- L'ajout de nouvelles commandes au bot met automatiquement à jour le module `!help` pour inclure les nouvelles fonctionnalités.

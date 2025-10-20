# Système d'Aide par Réaction

## Description

Le système d'aide par réaction permet aux apprenants de demander de l'aide en réagissant à un message avec l'emoji 🆘. Le bot contacte automatiquement un Helper aléatoire qui peut accepter ou refuser d'aider. Si le Helper refuse, le bot contacte automatiquement un autre Helper jusqu'à ce qu'un soit disponible.

## Configuration

### Prérequis

- Le rôle Helper doit être configuré dans `data/config.json` avec la clé `role_help`
- Le bot doit avoir les permissions pour envoyer des messages privés

### Installation

1. Le cog `reaction_help_cog` est déjà chargé automatiquement au démarrage du bot
2. Créez un message de demande d'aide avec la commande slash `/setup_reaction_help`

## Utilisation

### Pour les Administrateurs

**Créer un message de demande d'aide :**
```
/setup_reaction_help #canal
```
Cette commande va créer un message avec un embed dans le canal spécifié. Les utilisateurs pourront réagir à ce message avec 🆘 pour demander de l'aide.

### Pour les Apprenants

1. Trouvez le message de demande d'aide dans votre canal
2. Cliquez sur la réaction 🆘
3. Vous recevrez un message de confirmation en MP
4. Un Helper sera contacté automatiquement
5. Quand un Helper accepte, vous recevrez ses coordonnées en MP

### Pour les Helpers

1. Vous recevrez un MP du bot quand quelqu'un demande de l'aide
2. Le message contient le nom de la personne qui a besoin d'aide
3. Répondez au MP avec :
   - `oui` ou `yes` : pour accepter d'aider
   - `non` ou `no` : pour refuser (un autre Helper sera contacté)

4. Si vous acceptez :
   - Vous recevrez les coordonnées de la personne
   - La personne recevra vos coordonnées
   - Contactez la personne pour l'aider

5. Si vous refusez :
   - Un autre Helper sera contacté automatiquement
   - Aucune action supplémentaire n'est requise

## Fonctionnement Technique

### Flux de travail

1. **Demande d'aide** : Un apprenant réagit avec 🆘 au message de demande d'aide
2. **Sélection d'un Helper** : Le bot sélectionne aléatoirement un Helper qui n'a pas encore été contacté pour cette demande
3. **Contact du Helper** : Le bot envoie un MP au Helper avec les détails de la demande
4. **Réponse du Helper** :
   - Si `oui` : Le bot met en relation l'apprenant et le Helper, puis ferme la demande
   - Si `non` : Le bot contacte un autre Helper aléatoire
5. **Gestion des échecs** : Si tous les Helpers ont été contactés et aucun n'est disponible, l'apprenant est informé

### Stockage des données

Les demandes d'aide en cours sont stockées dans `data/help_requests.json` avec la structure suivante :
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

### Gestion des MPs

Le fichier `utils/handlers.py` gère les messages privés reçus par le bot :
- Si le message est une réponse à une demande d'aide (`oui`/`non`), il est traité par le système d'aide
- Sinon, il est enregistré dans Notion comme auparavant

## Avantages

- **Automatique** : Aucune intervention manuelle nécessaire
- **Équitable** : Sélection aléatoire des Helpers
- **Résilient** : Si un Helper refuse, un autre est contacté automatiquement
- **Traçable** : Toutes les demandes sont stockées et trackées

## Limitations

- Le bot doit pouvoir envoyer des MPs aux Helpers (ils doivent autoriser les MPs du serveur)
- Si aucun Helper n'est disponible, la demande est annulée (l'apprenant devra réessayer plus tard)

## Support

Pour toute question ou problème, contactez les administrateurs du serveur.

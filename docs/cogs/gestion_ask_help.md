# 🛠️ Documentation de la Commande `/send_help_embed`

## Description

La commande `/send_help_embed` permet d'envoyer un message d'aide dans un canal spécifique. Le message inclut un embed avec un bouton pour demander de l'aide. Selon le rôle de l'utilisateur, le message est envoyé dans un canal déterminé.

## Utilisation

**Commande :** `/send_help_embed`

### Paramètres

- **channel** *(Type : `TextChannel`)* : Le canal où l'embed d'aide sera envoyé.

### Fonctionnement

1. **Envoi de l'Embed :** La commande envoie un embed dans le canal spécifié avec une description invitant les membres à demander de l'aide en cliquant sur le bouton ci-dessous.
2. **Ajout de la Vue (View) :** Un bouton pour demander de l'aide est inclus dans l'embed. Lorsque ce bouton est cliqué, un message d'aide est posté dans un canal approprié en fonction des rôles de l'utilisateur.
3. **Réponses et Réactions :** La commande ajoute des réactions au message pour simuler un sondage ou des réponses.

### Exemple

```markdown
/send_embed_help channel:<#123456789012345678>
```
# ✨ Documentation de la Commande `/create_embed`

## Description

La commande `/create_embed` permet de créer un embed personnalisé. L'utilisateur remplit un formulaire avec des informations telles que le titre, la description, le pied de page, le nombre de sessions et le maximum de personnes par session. L'embed est ensuite envoyé dans le canal d'origine de la commande.

## Utilisation

**Commande :** `/create_embed`

### Paramètres

- **channel** *(Type : `TextChannel`)* : Le canal où l'embed de demande de session sera envoyé.

### Fonctionnement

1. **Formulaire de Création :** Un modal est présenté à l'utilisateur pour entrer les informations suivantes :
   - **Event Title** *(Titre de l'événement)* 🎉
   - **Description** *(Description de l'événement)* 📝
   - **Footer** *(Pied de page de l'embed)* 📜
   - **Number of Sessions** *(Nombre de sessions)* 🔢
   - **How much by session** *(Nombre maximum de personnes par session)* 👥

2. **Envoi de l'Embed :** Une fois le formulaire soumis, l'embed est créé avec les informations fournies et est envoyé dans le canal où la commande a été exécutée.
3. **Ajout de Réactions :** Des réactions sont ajoutées à l'embed pour permettre aux utilisateurs de voter ou de répondre au sondage. ✅

### Exemple

```markdown
/create_embed channel:<#123456789012345678>
```

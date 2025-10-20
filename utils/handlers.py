import discord
from discord import DMChannel
from utils.models import add_response_to_notion
from utils.logger import logger

async def handle_dm(bot, message):
    """Gère les messages privés reçus par le bot"""
    if isinstance(message.channel, DMChannel) and not message.author.bot:
        # Les réponses des Helpers sont maintenant gérées par réactions
        # Ce handler gère uniquement les autres messages DM (ex: Notion)
        try:
            user = message.author.name
            response = message.content

            add_response_to_notion(user, response)

            await message.channel.send("✅ Réponse enregistrée, merci !")
            logger.info(f"Réponse Notion enregistrée de {user}", category="notion")

        except Exception as e:
            logger.error(f"Erreur Notion pour {message.author.name} : {e}", category="notion")
            await message.channel.send("❌ Une erreur est survenue lors de l'enregistrement.")
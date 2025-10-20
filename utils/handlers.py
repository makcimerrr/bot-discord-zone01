import discord
from discord import DMChannel
from utils.models import add_response_to_notion
import json
import os
from utils.logger import logger

HELP_REQUESTS_FILE = "data/help_requests.json"

def load_help_requests():
    """Charge les demandes d'aide depuis le fichier JSON"""
    if os.path.exists(HELP_REQUESTS_FILE):
        with open(HELP_REQUESTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_help_requests(help_requests):
    """Sauvegarde les demandes d'aide dans le fichier JSON"""
    with open(HELP_REQUESTS_FILE, 'w') as f:
        json.dump(help_requests, f, indent=2)

async def handle_helper_response(bot, message, help_requests):
    """Gère les réponses des Helpers (oui/non)"""

    response_lower = message.content.lower().strip()

    # Vérifier si le message est une réponse oui/non
    if response_lower not in ['oui', 'non', 'yes', 'no']:
        return False

    # Trouver la demande d'aide pour laquelle ce Helper a été contacté
    helper_id = message.author.id
    request_id = None

    for req_id, req_data in help_requests.items():
        if req_data.get('current_helper') == helper_id:
            request_id = req_id
            break

    if not request_id:
        # Ce n'est pas une réponse à une demande d'aide
        return False

    request_data = help_requests[request_id]
    user_id = request_data['user_id']
    guild_id = request_data['guild_id']

    # Récupérer l'utilisateur et le guild
    try:
        user = await bot.fetch_user(user_id)
        guild = bot.get_guild(guild_id)
    except:
        await message.channel.send("❌ Erreur : impossible de récupérer l'utilisateur ou le serveur.")
        return True

    if response_lower in ['oui', 'yes']:
        # Helper accepte d'aider
        await message.channel.send(
            f"✅ Merci ! Tu as accepté d'aider **{user.name}**.\n"
            f"Tu peux le contacter directement : {user.mention}\n\n"
            f"Bon courage ! 💪"
        )

        # Informer l'utilisateur qu'un Helper a accepté
        try:
            helper_name = message.author.name
            await user.send(
                f"🎉 Super nouvelle ! **{helper_name}** a accepté de t'aider !\n"
                f"Il/Elle va te contacter prochainement.\n\n"
                f"En attendant, n'hésite pas à le/la contacter : {message.author.mention}"
            )
            logger.success(f"Helper {helper_name} a accepté d'aider {user.name}", category="help_system")
        except discord.Forbidden:
            logger.warning(f"Impossible d'envoyer un MP à {user.name}", category="help_system")

        # Supprimer la demande d'aide
        del help_requests[request_id]
        save_help_requests(help_requests)

    else:  # 'non' ou 'no'
        # Helper refuse d'aider
        await message.channel.send(
            "✅ Pas de problème ! Un autre Helper va être contacté.\n"
            "Merci d'avoir répondu ! 😊"
        )

        # Contacter un autre Helper
        # On doit appeler la méthode contact_helper du cog
        from cogs.reaction_help_cog import ReactionHelpSystem

        # Récupérer le cog
        cog = bot.get_cog('ReactionHelpSystem')
        if cog:
            logger.info(f"Helper {message.author.name} a refusé, contact d'un autre Helper", category="help_system")
            await cog.contact_helper(user, guild, request_id)
        else:
            logger.error("ReactionHelpSystem cog introuvable", category="help_system")

    return True

async def handle_dm(bot, message):
    if isinstance(message.channel, DMChannel) and not message.author.bot:
        # Charger les demandes d'aide
        help_requests = load_help_requests()

        # Vérifier si c'est une réponse à une demande d'aide
        is_helper_response = await handle_helper_response(bot, message, help_requests)

        if is_helper_response:
            # C'était une réponse à une demande d'aide, pas besoin d'enregistrer dans Notion
            return

        # Sinon, enregistrer dans Notion comme avant
        try:
            user = message.author.name
            response = message.content

            add_response_to_notion(user, response)

            await message.channel.send("✅ Réponse enregistrée, merci !")
            logger.info(f"Réponse Notion enregistrée de {user}", category="notion")

        except Exception as e:
            logger.error(f"Erreur Notion pour {message.author.name} : {e}", category="notion")
            await message.channel.send("❌ Une erreur est survenue lors de l'enregistrement.")
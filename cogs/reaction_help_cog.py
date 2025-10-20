import discord
from discord import app_commands
from discord.ext import commands
import random
import json
import os
from utils.config_loader import role_help
from utils.logger import logger
from utils.utils_function import is_admin_slash

# Fichier pour stocker les demandes d'aide en cours
HELP_REQUESTS_FILE = "data/help_requests.json"

# Emoji pour demander de l'aide
HELP_EMOJI = "🆘"

class ReactionHelpSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_requests = self.load_help_requests()

    def load_help_requests(self):
        """Charge les demandes d'aide depuis le fichier JSON"""
        if os.path.exists(HELP_REQUESTS_FILE):
            with open(HELP_REQUESTS_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_help_requests(self):
        """Sauvegarde les demandes d'aide dans le fichier JSON"""
        with open(HELP_REQUESTS_FILE, 'w') as f:
            json.dump(self.help_requests, f, indent=2)

    @app_commands.command(name="setup_reaction_help", description="Configure le message de demande d'aide par réaction")
    @is_admin_slash()
    async def setup_reaction_help(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Envoie un message avec une réaction pour demander de l'aide"""

        embed = discord.Embed(
            title="🆘 Besoin d'aide ?",
            description=(
                "Si tu as besoin d'aide, réagis à ce message avec 🆘\n\n"
                "Un Helper sera automatiquement contacté et viendra te donner un coup de main !"
            ),
            color=0x002e7a,
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(
            text="Zone01",
            icon_url="https://zone01rouennormandie.org/wp-content/uploads/2024/03/01talent-profil-400x400-1.jpg"
        )

        message = await channel.send(embed=embed)
        await message.add_reaction(HELP_EMOJI)

        await interaction.response.send_message(
            f"✅ Message de demande d'aide configuré dans {channel.mention}",
            ephemeral=True
        )

    async def get_available_helpers(self, guild, excluded_helpers=None):
        """Récupère la liste des Helpers disponibles (excluant ceux déjà contactés)"""
        if excluded_helpers is None:
            excluded_helpers = []

        role = guild.get_role(role_help)
        if not role:
            return []

        # Filtrer les membres qui ont le rôle Helper et qui ne sont pas dans la liste excluded
        available_helpers = [
            member for member in role.members
            if member.id not in excluded_helpers and not member.bot
        ]

        return available_helpers

    async def contact_helper(self, user, guild, request_id):
        """Contacte un Helper aléatoire pour une demande d'aide"""

        # Récupérer la liste des Helpers déjà contactés pour cette demande
        excluded_helpers = self.help_requests.get(request_id, {}).get('contacted_helpers', [])

        # Récupérer les Helpers disponibles
        available_helpers = await self.get_available_helpers(guild, excluded_helpers)

        if not available_helpers:
            # Plus de Helpers disponibles
            try:
                await user.send(
                    "😔 Désolé, tous les Helpers ont été contactés mais aucun n'est disponible pour le moment. "
                    "Réessaie plus tard ou demande de l'aide dans les canaux publics."
                )
            except discord.Forbidden:
                logger.warning(f"Impossible d'envoyer un MP à {user.name}", category="help_system")

            # Supprimer la demande
            if request_id in self.help_requests:
                del self.help_requests[request_id]
                self.save_help_requests()

            return

        # Sélectionner un Helper aléatoire
        helper = random.choice(available_helpers)

        # Enregistrer le Helper contacté
        if request_id not in self.help_requests:
            self.help_requests[request_id] = {
                'user_id': user.id,
                'guild_id': guild.id,
                'contacted_helpers': []
            }

        self.help_requests[request_id]['contacted_helpers'].append(helper.id)
        self.help_requests[request_id]['current_helper'] = helper.id
        self.save_help_requests()

        # Créer le message pour le Helper
        embed = discord.Embed(
            title="🆘 Demande d'aide",
            description=(
                f"**{user.mention}** ({user.name}) a besoin d'aide !\n\n"
                f"Peux-tu l'aider cette semaine ?\n\n"
                f"**Réponds avec :**\n"
                f"✅ `oui` - Si tu es disponible\n"
                f"❌ `non` - Si tu n'es pas disponible\n\n"
                f"_ID de la demande : {request_id}_"
            ),
            color=0xff6b6b
        )

        try:
            await helper.send(embed=embed)
            logger.info(f"Helper {helper.name} contacté pour la demande {request_id}", category="help_system")
        except discord.Forbidden:
            logger.warning(f"Impossible d'envoyer un MP à {helper.name}", category="help_system")
            # Si on ne peut pas envoyer de MP au Helper, on en contacte un autre
            await self.contact_helper(user, guild, request_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Détecte quand quelqu'un ajoute une réaction au message d'aide"""

        # Ignorer les réactions du bot
        if payload.user_id == self.bot.user.id:
            return

        # Vérifier si c'est la bonne réaction
        if str(payload.emoji) != HELP_EMOJI:
            return

        # Récupérer le message, le channel et l'utilisateur
        channel = self.bot.get_channel(payload.channel_id)
        if not channel:
            return

        try:
            message = await channel.fetch_message(payload.message_id)
        except:
            return

        # Vérifier si le message est un message d'aide (contient "Besoin d'aide" dans l'embed)
        if not message.embeds or "Besoin d'aide" not in message.embeds[0].title:
            return

        user = await self.bot.fetch_user(payload.user_id)
        guild = self.bot.get_guild(payload.guild_id)

        # Retirer la réaction de l'utilisateur pour qu'il puisse la rajouter plus tard
        try:
            await message.remove_reaction(payload.emoji, user)
        except:
            pass

        # Créer un ID unique pour cette demande
        request_id = f"{user.id}_{payload.message_id}"

        # Vérifier si une demande est déjà en cours pour cet utilisateur
        if request_id in self.help_requests:
            try:
                await user.send(
                    "⏳ Tu as déjà une demande d'aide en cours. Un Helper va bientôt te contacter !"
                )
            except discord.Forbidden:
                pass
            return

        # Envoyer un message de confirmation à l'utilisateur
        try:
            await user.send(
                "✅ Ta demande d'aide a été enregistrée ! Un Helper va être contacté et viendra vers toi."
            )
            logger.success(f"Nouvelle demande d'aide de {user.name} (ID: {request_id})", category="help_system")
        except discord.Forbidden:
            logger.warning(f"Impossible d'envoyer un MP à {user.name}", category="help_system")

        # Contacter un Helper
        await self.contact_helper(user, guild, request_id)

async def setup(bot):
    await bot.add_cog(ReactionHelpSystem(bot))

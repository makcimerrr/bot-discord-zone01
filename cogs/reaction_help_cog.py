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
                f"**Réagis à ce message :**\n"
                f"✅ Si tu es disponible\n"
                f"❌ Si tu n'es pas disponible\n\n"
                f"_ID de la demande : {request_id}_"
            ),
            color=0xff6b6b
        )

        try:
            dm_message = await helper.send(embed=embed)
            # Ajouter les réactions au message
            await dm_message.add_reaction("✅")
            await dm_message.add_reaction("❌")

            # Enregistrer le message ID pour le tracking
            self.help_requests[request_id]['message_id'] = dm_message.id
            self.save_help_requests()

            logger.info(f"Helper {helper.name} contacté pour la demande {request_id}", category="help_system")
        except discord.Forbidden:
            logger.warning(f"Impossible d'envoyer un MP à {helper.name}", category="help_system")
            # Si on ne peut pas envoyer de MP au Helper, on en contacte un autre
            await self.contact_helper(user, guild, request_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Détecte les réactions (demandes d'aide et réponses des Helpers)"""

        # Ignorer les réactions du bot
        if payload.user_id == self.bot.user.id:
            return

        # CAS 1 : Réaction dans un DM (réponse du Helper)
        if payload.guild_id is None:
            logger.info(f"Réaction DM détectée: {payload.emoji} de user {payload.user_id} sur message {payload.message_id}", category="help_system")

            # Vérifier si c'est une réaction valide (✅ ou ❌)
            if str(payload.emoji) not in ["✅", "❌"]:
                logger.info(f"Réaction ignorée: emoji non valide {payload.emoji}", category="help_system")
                return

            logger.info(f"Recherche de la demande correspondante parmi {len(self.help_requests)} demandes", category="help_system")
            logger.info(f"Contenu help_requests: {self.help_requests}", category="help_system")

            # Chercher la demande correspondante
            request_id = None
            for req_id, req_data in self.help_requests.items():
                if req_data.get('message_id') == payload.message_id and req_data.get('current_helper') == payload.user_id:
                    request_id = req_id
                    break

            if not request_id:
                logger.warning(f"Aucune demande trouvée pour message_id={payload.message_id} et current_helper={payload.user_id}", category="help_system")
                return

            logger.success(f"Demande trouvée: {request_id}", category="help_system")

            request_data = self.help_requests[request_id]

            # Vérifier si la demande a déjà été traitée (éviter les doubles clics)
            if request_data.get('response_processed', False):
                return

            user_id = request_data['user_id']
            guild_id = request_data['guild_id']

            # Récupérer l'utilisateur et le guild
            try:
                user = await self.bot.fetch_user(user_id)
                guild = self.bot.get_guild(guild_id)
                helper = await self.bot.fetch_user(payload.user_id)
            except:
                logger.error("Impossible de récupérer l'utilisateur ou le serveur", category="help_system")
                return

            # Récupérer le channel DM et le message
            try:
                dm_channel = await helper.create_dm()
                message = await dm_channel.fetch_message(payload.message_id)

                # Supprimer immédiatement toutes les réactions pour verrouiller le choix
                await message.clear_reactions()
            except:
                logger.error("Impossible de récupérer le message DM", category="help_system")
                return

            if str(payload.emoji) == "✅":
                # Marquer comme traitée pour éviter les doubles clics
                self.help_requests[request_id]['response_processed'] = True
                self.save_help_requests()

                # Helper accepte d'aider
                await message.edit(embed=discord.Embed(
                    title="✅ Demande Acceptée",
                    description=(
                        f"Merci ! Tu as accepté d'aider **{user.name}**.\n\n"
                        f"**Coordonnées du demandeur :**\n"
                        f"• Nom : {user.name}\n"
                        f"• ID Discord : {user.id}\n"
                        f"• Mention : {user.mention}\n\n"
                        f"Tu peux maintenant le contacter en MP pour lui proposer ton aide !\n"
                        f"Bon courage ! 💪\n\n"
                        f"_Votre choix a été enregistré et ne peut plus être modifié._"
                    ),
                    color=0x00ff00
                ))

                # Informer l'utilisateur qu'un Helper a accepté
                try:
                    await user.send(
                        f"🎉 Super nouvelle ! **{helper.name}** a accepté de t'aider !\n"
                        f"Il/Elle va te contacter prochainement.\n\n"
                        f"Tu peux aussi le/la contacter directement : {helper.mention}"
                    )
                    logger.success(f"Helper {helper.name} a accepté d'aider {user.name}", category="help_system")
                except discord.Forbidden:
                    logger.warning(f"Impossible d'envoyer un MP à {user.name}", category="help_system")

                # Supprimer la demande d'aide
                del self.help_requests[request_id]
                self.save_help_requests()

            else:  # ❌
                # Marquer comme traitée pour ce helper spécifique
                self.help_requests[request_id]['response_processed'] = True
                self.save_help_requests()

                # Helper refuse d'aider
                await message.edit(embed=discord.Embed(
                    title="❌ Demande Refusée",
                    description=(
                        "Pas de problème ! Un autre Helper va être contacté.\n"
                        "Merci d'avoir répondu ! 😊\n\n"
                        f"_Votre choix a été enregistré et ne peut plus être modifié._"
                    ),
                    color=0xff0000
                ))

                logger.info(f"Helper {helper.name} a refusé, contact d'un autre Helper", category="help_system")

                # Réinitialiser le flag pour permettre au prochain helper de répondre
                self.help_requests[request_id]['response_processed'] = False
                self.help_requests[request_id].pop('current_helper', None)
                self.help_requests[request_id].pop('message_id', None)
                self.save_help_requests()

                # Contacter un autre Helper
                await self.contact_helper(user, guild, request_id)

            return

        # CAS 2 : Réaction dans un channel (demande d'aide initiale)
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

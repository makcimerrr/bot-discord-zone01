import os
import json
from pathlib import Path
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from utils.utils_function import is_admin, is_admin_slash
from utils.logger import logger

CONFIG_FILE = "data/config.json"


class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_config(self):
        """Charge la configuration depuis le fichier JSON"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self, config):
        """Sauvegarde la configuration dans le fichier JSON"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        logger.success("Configuration sauvegardée", category="config")

    @commands.command(name='showqueryIntern')
    @is_admin()
    async def show_query_intern(self, ctx):
        """Commande pour afficher la query actuelle pour les alternances/stages."""
        env_path = Path('../.env')  # Charger le fichier .env situé à la racine du projet
        load_dotenv(dotenv_path=env_path, override=True)
        query_intern = os.getenv('QUERY_INTERNSHIP')  # Récupérer la variable mise à jour

        if not query_intern or query_intern == "":
            embed = discord.Embed(
                title="❌ Aucune Query Définie",
                description="Aucune query n'a été définie. Utilisez la commande `!setqueryIntern` pour en définir une.",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="🔍 Query Actuelle",
                description=f"La query actuelle est : **{query_intern}**",
                color=discord.Color.blue()
            )

        await ctx.send(embed=embed)

    @commands.command(name='showqueryFulltime')
    @is_admin()
    async def show_query_fulltime(self, ctx):
        """Commande pour afficher la query actuelle pour les emplois à temps plein."""
        env_path = Path('../.env')  # Charger le fichier .env situé à la racine du projet
        load_dotenv(dotenv_path=env_path, override=True)
        query_fulltime = os.getenv('QUERY_FULLTIME')  # Récupérer la variable mise à jour
        if not query_fulltime or query_fulltime == "":
            embed = discord.Embed(
                title="❌ Aucune Query Définie",
                description="Aucune query n'a été définie. Utilisez la commande `!setqueryFulltime` pour en définir une.",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="🔍 Query Actuelle",
                description=f"La query actuelle est : **{query_fulltime}**",
                color=discord.Color.blue()
            )

        await ctx.send(embed=embed)

    @app_commands.command(name="show_config", description="Affiche un résumé de la configuration du bot")
    @is_admin_slash()
    async def show_config(self, interaction: discord.Interaction):
        """Affiche la configuration actuelle du bot sous forme d'embed"""
        if interaction.guild is None:
            await interaction.response.send(content="❌ Cette commande ne peut pas être utilisée en message privé.", ephemeral=True)
            return

        config = self.load_config()

        embed = discord.Embed(
            title="⚙️ Configuration du Bot",
            description="Configuration actuelle des canaux et rôles",
            color=0x002e7a,
            timestamp=discord.utils.utcnow()
        )

        # Serveur
        guild = interaction.guild
        if guild and config.get('guild_id') == guild.id:
            embed.add_field(
                name="🏠 Serveur",
                value=f"**Nom:** {guild.name}\n**ID:** {guild.id}",
                inline=False
            )

        # Canaux généraux
        channels_info = []
        general_channel_keys = [
            ("channel_inter_promo", "Canal Inter-Promo"),
            ("forum_channel_id", "Forum Alternances"),
            ("forum_channel_id_cdi", "Forum CDI")
        ]

        for key, label in general_channel_keys:
            channel_id = config.get(key)
            if channel_id:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    channels_info.append(f"**{label}:** {channel.mention}")
                else:
                    channels_info.append(f"**{label}:** ID `{channel_id}` (non trouvé)")

        if channels_info:
            embed.add_field(
                name="📺 Canaux Généraux",
                value="\n".join(channels_info),
                inline=False
            )

        # Rôles généraux
        roles_info = []
        general_role_keys = [
            ("role_help", "Helper"),
            ("role_ping_cdi", "Ping CDI"),
            ("role_ping_alternance", "Ping Alternance")
        ]

        for key, label in general_role_keys:
            role_id = config.get(key)
            if role_id:
                role = guild.get_role(role_id) if guild else None
                if role:
                    roles_info.append(f"**{label}:** {role.mention}")
                else:
                    roles_info.append(f"**{label}:** ID `{role_id}` (non trouvé)")

        if roles_info:
            embed.add_field(
                name="👥 Rôles Généraux",
                value="\n".join(roles_info),
                inline=False
            )

        # Promotions (détection dynamique)
        promotions = {}
        for key in config:
            if key.startswith("channel_progress_"):
                promo_name = key.replace("channel_progress_", "").replace("_", " ")
                if promo_name not in promotions:
                    promotions[promo_name] = {}
                promotions[promo_name]["channel"] = config[key]
            elif key.startswith("role_") and key not in ["role_help", "role_ping_cdi", "role_ping_alternance"]:
                promo_name = key.replace("role_", "").replace("_", " ").title()
                if promo_name not in promotions:
                    promotions[promo_name] = {}
                promotions[promo_name]["role"] = config[key]

        if promotions:
            promo_info = []
            for promo_name in sorted(promotions.keys()):
                promo_data = promotions[promo_name]
                info_parts = [f"**{promo_name}:**"]

                # Canal
                if "channel" in promo_data:
                    channel_id = promo_data["channel"]
                    channel = self.bot.get_channel(channel_id)
                    if channel:
                        info_parts.append(f"  📺 {channel.mention}")
                    else:
                        info_parts.append(f"  📺 ID `{channel_id}` (non trouvé)")

                # Rôle
                if "role" in promo_data:
                    role_id = promo_data["role"]
                    role = guild.get_role(role_id) if guild else None
                    if role:
                        info_parts.append(f"  👥 {role.mention}")
                    else:
                        info_parts.append(f"  👥 ID `{role_id}` (non trouvé)")

                promo_info.append("\n".join(info_parts))

            embed.add_field(
                name="📚 Promotions",
                value="\n".join(promo_info),
                inline=False
            )

        embed.set_footer(
            text="Zone01",
            icon_url="https://zone01rouennormandie.org/wp-content/uploads/2024/03/01talent-profil-400x400-1.jpg"
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Configuration affichée par {interaction.user.name}", category="config")

    @app_commands.command(name="add_promotion", description="Ajoute une nouvelle promotion avec son canal et rôle")
    @is_admin_slash()
    @app_commands.describe(
        promotion_name="Le nom de la promotion (ex: P2 2025, P1 2026)",
        channel="Le canal de progression (mention #canal ou ID)",
        role="Le rôle de la promotion (mention @role ou ID)"
    )
    async def add_promotion(self, interaction: discord.Interaction, promotion_name: str, channel: str, role: str):
        """Ajoute une nouvelle configuration de promotion avec son canal et rôle"""
        if interaction.guild is None:
            await interaction.response.send(content="❌ Cette commande ne peut pas être utilisée en message privé.", ephemeral=True)
            return

        import re

        config = self.load_config()

        # Créer les clés de configuration basées sur le nom de la promotion
        channel_config_key = f"channel_progress_{promotion_name.replace(' ', '_')}"
        role_config_key = f"role_{promotion_name.replace(' ', '_').lower()}"

        # Extraire l'ID du canal
        channel_id = None

        # Vérifier si c'est une mention de canal (<#123456789>)
        channel_match = re.match(r'<#(\d+)>', channel)
        if channel_match:
            channel_id = int(channel_match.group(1))
        else:
            # Sinon, essayer de parser comme un nombre
            try:
                channel_id = int(channel)
            except ValueError:
                await interaction.response.send_message(
                    f"❌ Erreur : Le canal doit être un ID valide ou une mention de canal (#canal).\n"
                    f"Exemples :\n"
                    f"• ID direct : `1234567890123456789`\n"
                    f"• Mention de canal : `#progression-p2-2025`",
                    ephemeral=True
                )
                return

        # Extraire l'ID du rôle
        role_id = None

        # Vérifier si c'est une mention de rôle (<@&123456789>)
        role_match = re.match(r'<@&(\d+)>', role)
        if role_match:
            role_id = int(role_match.group(1))
        else:
            # Sinon, essayer de parser comme un nombre
            try:
                role_id = int(role)
            except ValueError:
                await interaction.response.send_message(
                    f"❌ Erreur : Le rôle doit être un ID valide ou une mention de rôle (@role).\n"
                    f"Exemples :\n"
                    f"• ID direct : `1234567890123456789`\n"
                    f"• Mention de rôle : `@P2 2025`",
                    ephemeral=True
                )
                return

        # Vérifier si la promotion existe déjà
        if channel_config_key in config or role_config_key in config:
            await interaction.response.send_message(
                f"⚠️ La promotion `{promotion_name}` existe déjà.\n"
                f"Utilisez `/edit_config` pour la modifier.",
                ephemeral=True
            )
            return

        # Vérifier que le canal existe
        channel_obj = self.bot.get_channel(channel_id)
        channel_warning = None
        if not channel_obj:
            channel_warning = f"⚠️ Le canal avec l'ID `{channel_id}` n'a pas été trouvé."

        # Vérifier que le rôle existe
        role_obj = interaction.guild.get_role(role_id) if interaction.guild else None
        role_warning = None
        if not role_obj:
            role_warning = f"⚠️ Le rôle avec l'ID `{role_id}` n'a pas été trouvé."

        # Ajouter la nouvelle promotion à la config
        config[channel_config_key] = channel_id
        config[role_config_key] = role_id
        self.save_config(config)

        # Construire le message de confirmation
        embed = discord.Embed(
            title="✅ Promotion Ajoutée",
            description=f"La promotion `{promotion_name}` a été configurée avec succès",
            color=0x00ff00,
            timestamp=discord.utils.utcnow()
        )

        embed.add_field(name="📚 Promotion", value=f"`{promotion_name}`", inline=False)
        embed.add_field(name="🔑 Clé canal", value=f"`{channel_config_key}`", inline=False)
        embed.add_field(name="🔑 Clé rôle", value=f"`{role_config_key}`", inline=False)

        # Information sur le canal
        if channel_obj:
            embed.add_field(
                name="📺 Canal",
                value=f"{channel_obj.mention} ({channel_obj.name})",
                inline=True
            )
        else:
            embed.add_field(
                name="📺 Canal ID",
                value=f"`{channel_id}`",
                inline=True
            )

        # Information sur le rôle
        if role_obj:
            embed.add_field(
                name="👥 Rôle",
                value=f"{role_obj.mention} ({role_obj.name})",
                inline=True
            )
        else:
            embed.add_field(
                name="👥 Rôle ID",
                value=f"`{role_id}`",
                inline=True
            )

        # Ajouter les avertissements s'il y en a
        if channel_warning or role_warning:
            warnings = []
            if channel_warning:
                warnings.append(channel_warning)
            if role_warning:
                warnings.append(role_warning)
            embed.add_field(
                name="⚠️ Avertissements",
                value="\n".join(warnings),
                inline=False
            )

        embed.set_footer(text="La promotion est maintenant disponible pour le suivi automatique")

        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.success(f"Promotion ajoutée par {interaction.user.name}: {promotion_name} -> canal:{channel_id}, rôle:{role_id}", category="config")

    @app_commands.command(name="edit_config", description="Édite la configuration du bot (IDs de canaux ou rôles)")
    @is_admin_slash()
    @app_commands.describe(
        key="La clé de configuration à modifier",
        value="ID, mention de canal (#canal) ou mention de rôle (@role)"
    )
    @app_commands.choices(key=[
        app_commands.Choice(name="Canal Inter-Promo", value="channel_inter_promo"),
        app_commands.Choice(name="Forum Alternances", value="forum_channel_id"),
        app_commands.Choice(name="Forum CDI", value="forum_channel_id_cdi"),
        app_commands.Choice(name="Rôle Helper", value="role_help"),
        app_commands.Choice(name="Rôle Ping CDI", value="role_ping_cdi"),
        app_commands.Choice(name="Rôle Ping Alternance", value="role_ping_alternance"),
        app_commands.Choice(name="Rôle P1 2023", value="role_p1_2023"),
        app_commands.Choice(name="Rôle P2 2023", value="role_p2_2023"),
        app_commands.Choice(name="Rôle P1 2024", value="role_p1_2024"),
        app_commands.Choice(name="Canal Progression P1 2022", value="channel_progress_P1_2022"),
        app_commands.Choice(name="Canal Progression P1 2023", value="channel_progress_P1_2023"),
        app_commands.Choice(name="Canal Progression P2 2023", value="channel_progress_P2_2023"),
        app_commands.Choice(name="Canal Progression P1 2024", value="channel_progress_P1_2024"),
        app_commands.Choice(name="Canal Progression P1 2025", value="channel_progress_P1_2025"),
        app_commands.Choice(name="ID du Serveur", value="guild_id")
    ])
    async def edit_config(self, interaction: discord.Interaction, key: str, value: str):
        """Édite une valeur de configuration"""
        if interaction.guild is None:
            await interaction.response.send(content="❌ Cette commande ne peut pas être utilisée en message privé.", ephemeral=True)
            return

        import re

        config = self.load_config()

        # Extraire l'ID depuis les mentions ou utiliser l'ID directement
        value_int = None

        # Vérifier si c'est une mention de canal (<#123456789>)
        channel_match = re.match(r'<#(\d+)>', value)
        if channel_match:
            value_int = int(channel_match.group(1))

        # Vérifier si c'est une mention de rôle (<@&123456789>)
        if not value_int:
            role_match = re.match(r'<@&(\d+)>', value)
            if role_match:
                value_int = int(role_match.group(1))

        # Si ce n'est pas une mention, essayer de parser comme un nombre
        if not value_int:
            try:
                value_int = int(value)
            except ValueError:
                await interaction.response.send_message(
                    f"❌ Erreur : La valeur doit être un ID valide, une mention de canal (#canal) ou une mention de rôle (@role).\n"
                    f"Exemples :\n"
                    f"• ID direct : `1234567890123456789`\n"
                    f"• Mention de canal : `#general`\n"
                    f"• Mention de rôle : `@Helper`",
                    ephemeral=True
                )
                return

        # Récupérer l'ancienne valeur
        old_value = config.get(key, "Non définie")

        # Mettre à jour la configuration
        config[key] = value_int
        self.save_config(config)

        # Construire le message de confirmation
        embed = discord.Embed(
            title="✅ Configuration Mise à Jour",
            description=f"La configuration a été mise à jour avec succès",
            color=0x00ff00,
            timestamp=discord.utils.utcnow()
        )

        embed.add_field(name="Clé", value=f"`{key}`", inline=False)
        embed.add_field(name="Ancienne valeur", value=f"`{old_value}`", inline=True)
        embed.add_field(name="Nouvelle valeur", value=f"`{value_int}`", inline=True)

        # Vérifier si l'ID correspond à un canal ou rôle existant
        if key.startswith("channel") or key.startswith("forum"):
            channel = self.bot.get_channel(value_int)
            if channel:
                embed.add_field(
                    name="✅ Canal trouvé",
                    value=f"{channel.mention} ({channel.name})",
                    inline=False
                )
            else:
                embed.add_field(
                    name="⚠️ Avertissement",
                    value="Le canal avec cet ID n'a pas été trouvé. Vérifiez que l'ID est correct.",
                    inline=False
                )
        elif key.startswith("role"):
            role = interaction.guild.get_role(value_int) if interaction.guild else None
            if role:
                embed.add_field(
                    name="✅ Rôle trouvé",
                    value=f"{role.mention} ({role.name})",
                    inline=False
                )
            else:
                embed.add_field(
                    name="⚠️ Avertissement",
                    value="Le rôle avec cet ID n'a pas été trouvé. Vérifiez que l'ID est correct.",
                    inline=False
                )

        embed.set_footer(text="Les changements sont appliqués immédiatement")

        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.success(f"Configuration modifiée par {interaction.user.name}: {key} = {value_int}", category="config")


async def setup(bot):
    await bot.add_cog(Configuration(bot))

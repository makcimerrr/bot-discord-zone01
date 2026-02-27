import asyncio
import base64
import requests
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Modal, TextInput, View, Button

from utils.logger import logger

ZONE01_DOMAIN = "zone01normandie.org"
ZONE01_API_URL = "https://api-zone01-rouen.deno.dev/api/v1"


def _auth_zone01(login: str, password: str) -> tuple[bool, int]:
    """Authentifie l'utilisateur auprès de l'API Zone01 (synchrone, appelé via asyncio.to_thread)."""
    credentials = base64.b64encode(f"{login}:{password}".encode()).decode()
    try:
        response = requests.post(
            f"https://{ZONE01_DOMAIN}/api/auth/signin",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {credentials}",
            },
            timeout=10,
        )
        return response.ok, response.status_code
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur réseau lors de l'authentification : {e}")


def _link_discord_user(login: str, discord_id: str) -> tuple[bool, int]:
    """Envoie le login + discord_id à l'API Zone01 (synchrone, appelé via asyncio.to_thread)."""
    try:
        response = requests.put(
            f"{ZONE01_API_URL}/discord-users",
            json={"login": login, "discord_id": discord_id},
            timeout=10,
        )
        return response.ok, response.status_code
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur réseau lors de la liaison de compte : {e}")


class ConnectModal(Modal, title="Connexion Zone01"):
    login = TextInput(
        label="Login Zone01",
        placeholder="Votre identifiant Zone01",
        required=True,
        max_length=50,
    )
    password = TextInput(
        label="Mot de passe",
        placeholder="Votre mot de passe Zone01",
        required=True,
        max_length=100,
        style=discord.TextStyle.short,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        login_value = self.login.value.strip()
        discord_id = str(interaction.user.id)

        # Étape 1 : Authentification Zone01
        try:
            auth_ok, auth_status = await asyncio.to_thread(
                _auth_zone01, login_value, self.password.value
            )
        except RuntimeError as e:
            embed = discord.Embed(
                title="❌ Erreur de connexion",
                description="Une erreur réseau est survenue. Veuillez réessayer plus tard.",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.error(f"Erreur réseau pour {interaction.user.name} : {e}", category="connect")
            return

        if not auth_ok:
            embed = discord.Embed(
                title="❌ Identifiants invalides",
                description=f"Le login ou le mot de passe est incorrect (HTTP {auth_status}). Veuillez réessayer.",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.warning(
                f"Échec d'authentification pour {interaction.user.name} — login: {login_value}",
                category="connect",
            )
            return

        # Étape 2 : Liaison Discord ↔ Zone01
        try:
            api_ok, api_status = await asyncio.to_thread(
                _link_discord_user, login_value, discord_id
            )
        except RuntimeError as e:
            embed = discord.Embed(
                title="❌ Erreur API",
                description="L'authentification a réussi mais une erreur est survenue lors de l'enregistrement. Veuillez réessayer.",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.error(
                f"Erreur API lors de la liaison pour {interaction.user.name} : {e}", category="connect"
            )
            return

        if not api_ok:
            embed = discord.Embed(
                title="❌ Erreur API",
                description=f"Impossible d'enregistrer la liaison (HTTP {api_status}). Veuillez réessayer plus tard.",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.error(
                f"API returned {api_status} pour {interaction.user.name} — login: {login_value}",
                category="connect",
            )
            return

        # Succès
        embed = discord.Embed(
            title="✅ Compte lié avec succès !",
            description=f"Votre compte Discord est maintenant lié à votre compte Zone01 **{login_value}**.",
            color=discord.Color.green(),
        )
        embed.set_footer(text="Vous pouvez relancer /connect à tout moment pour mettre à jour la liaison.")
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.success(
            f"Liaison réussie : Zone01={login_value} ↔ Discord={interaction.user.name} ({discord_id})",
            category="connect",
        )

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        logger.error(f"Erreur inattendue dans ConnectModal : {error}", category="connect")
        try:
            await interaction.response.send_message(
                "❌ Une erreur inattendue s'est produite. Veuillez réessayer.", ephemeral=True
            )
        except discord.InteractionResponded:
            await interaction.followup.send(
                "❌ Une erreur inattendue s'est produite. Veuillez réessayer.", ephemeral=True
            )


class ConnectView(View):
    def __init__(self):
        super().__init__(timeout=300)  # Bouton valide 5 minutes

    @discord.ui.button(label="Se connecter", style=discord.ButtonStyle.primary, emoji="🔗")
    async def connect_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(ConnectModal())


class ConnectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="connect",
        description="Liez votre compte Discord à votre compte Zone01",
    )
    async def connect(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🔗 Liaison de compte Zone01",
            description=(
                "Cliquez sur le bouton ci-dessous pour lier votre compte Discord "
                "à votre compte Zone01.\n\n"
                "**Vos identifiants ne sont jamais stockés** — ils servent uniquement "
                "à vérifier votre identité auprès de Zone01."
            ),
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="ℹ️ Comment ça marche ?",
            value=(
                "1. Cliquez sur **Se connecter**\n"
                "2. Entrez votre login et mot de passe Zone01\n"
                "3. Votre compte est lié automatiquement !"
            ),
            inline=False,
        )
        embed.set_footer(text="Vous pouvez relancer /connect à tout moment pour mettre à jour la liaison.")

        await interaction.response.send_message(embed=embed, view=ConnectView(), ephemeral=True)
        logger.info(
            f"Commande /connect lancée par {interaction.user.name} ({interaction.user.id})",
            category="connect",
        )


async def setup(bot):
    await bot.add_cog(ConnectCog(bot))

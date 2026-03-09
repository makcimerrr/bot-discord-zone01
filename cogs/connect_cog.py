import discord
from discord import app_commands
from discord.ext import commands

from utils.logger import logger
from utils.web_server import create_connect_token


class ConnectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="connect",
        description="Liez votre compte Discord à votre compte Zone01",
    )
    async def connect(self, interaction: discord.Interaction):
        connect_base_url = self.bot.connect_base_url
        token = create_connect_token(str(interaction.user.id))
        link = f"{connect_base_url}/connect?token={token}"

        embed = discord.Embed(
            title="🔗 Liaison de compte Zone01",
            description=(
                "Cliquez sur le bouton ci-dessous pour lier votre compte Discord "
                "à votre compte Zone01.\n\n"
                "Vous serez redirigé vers une page web sécurisée où vous entrerez "
                "vos identifiants **directement dans votre navigateur** — "
                "vos identifiants ne transitent jamais par Discord."
            ),
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="ℹ️ Comment ça marche ?",
            value=(
                "1. Cliquez sur **Lier mon compte**\n"
                "2. Entrez votre login et mot de passe Zone01 sur la page web\n"
                "3. Recevez une confirmation par DM ici !"
            ),
            inline=False,
        )
        embed.set_footer(text="Ce lien est à usage unique et expire dans 10 minutes.")

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Lier mon compte",
                url=link,
                style=discord.ButtonStyle.link,
                emoji="🔗",
            )
        )

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        logger.info(
            f"Lien /connect généré pour {interaction.user.name} ({interaction.user.id})",
            category="connect",
        )


async def setup(bot):
    await bot.add_cog(ConnectCog(bot))

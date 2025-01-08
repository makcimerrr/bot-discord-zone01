import os
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.utils_function import is_admin


class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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


async def setup(bot):
    await bot.add_cog(Configuration(bot))

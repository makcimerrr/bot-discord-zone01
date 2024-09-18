import discord
from discord.ext import commands
from utils.config_loader import query_intern, query_fulltime
from dotenv import set_key
from pathlib import Path
from utils.utils_function import get_query_intern, get_query_fulltime

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.query_intern = query_intern  # Initialiser avec la variable depuis .env
        self.query_fulltime = query_fulltime  # Ajouter la variable pour fulltime

    @commands.command(name='showqueryIntern')
    async def show_query_intern(self, ctx):
        """Commande pour afficher la query actuelle pour les alternances/stages."""
        if not self.query_intern:
            embed = discord.Embed(
                title="❌ Aucune Query Définie",
                description="Aucune query n'a été définie. Utilisez la commande `!setqueryIntern` pour en définir une.",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="🔍 Query Actuelle",
                description=f"La query actuelle est : **{self.query_intern}**",
                color=discord.Color.blue()
            )

        await ctx.send(embed=embed)

    @commands.command(name='showqueryFulltime')
    async def show_query_fulltime(self, ctx):
        """Commande pour afficher la query actuelle pour les emplois à temps plein."""
        if not self.query_fulltime:
            embed = discord.Embed(
                title="❌ Aucune Query Définie",
                description="Aucune query n'a été définie. Utilisez la commande `!setqueryFulltime` pour en définir une.",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="🔍 Query Actuelle",
                description=f"La query actuelle est : **{self.query_fulltime}**",
                color=discord.Color.blue()
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Configuration(bot))
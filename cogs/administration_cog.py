import discord
import re
import asyncio

from discord.ext import commands
from dotenv import set_key
from pathlib import Path

from utils.utils_function import get_query_intern, get_query_fulltime
from utils.config_loader import role_ping_cdi, forum_channel_id_cdi, role_p1_2023, role_p2_2023, forum_channel_id, guild_id, forbidden_words, technologies, query_intern, query_fulltime
from utils.cdi_fetcher import fetch_api_fulltime
from utils.intern_fetcher import fetch_api_intern
from utils.utils_internship import send_jobslist
from utils.utils_fulltime import send_cdilist

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.query_intern = query_intern  # Initialiser avec la variable depuis .env
        self.query_fulltime = query_fulltime  # Ajouter la variable pour fulltime
        self.forbidden_words = forbidden_words
        self.send_jobslist = send_jobslist
        self.send_cdilist = send_cdilist

    @commands.command(name='setqueryIntern')
    async def set_query_intern(self, ctx, query: str = None):
        """Commande pour définir une query de rechercher pour les alternances/stages."""
        if query is None:
            embed = discord.Embed(
                title="⚠️ Erreur : Query manquante",
                description="Veuillez fournir une query pour définir une nouvelle valeur. Utilisez `!setqueryIntern <query>`.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if not query.strip():
            embed = discord.Embed(
                title="⚠️ Erreur : Query vide",
                description="La query que vous avez fournie est vide. Veuillez entrer une query valide.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if query.strip() == "default":
            # Réinitialiser la query à la valeur par défaut
            self.query_intern = "Alternance Développeur Rouen"  # Mettre une valeur par défaut appropriée
            env_path = Path('.') / '.env'
            set_key(env_path, 'QUERY_INTERNSHIP', self.query_intern)

            embed = discord.Embed(
                title="🔄 Query Réinitialisée",
                description=f"La query a été réinitialisée à : **{self.query_intern}**",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return

        if query == self.query_intern:
            embed = discord.Embed(
                title="⚠️ Query Identique",
                description="La query que vous avez fournie est identique à la query actuelle. Veuillez fournir une nouvelle query.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if len(query) > 100:
            embed = discord.Embed(
                title="⚠️ Query Trop Longue",
                description="La query que vous avez fournie est trop longue. Veuillez fournir une query de 100 caractères ou moins.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Mettre à jour la variable et le fichier .env
        self.query_intern = query
        env_path = Path('.') / '.env'
        set_key(env_path, 'QUERY_INTERNSHIP', query)

        embed = discord.Embed(
            title="✅ Query Initialisée",
            description=f"La query a été définie comme : **{self.query_intern}**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name='setqueryFulltime')
    async def set_query_fulltime(self, ctx, query: str = None):
        """Commande pour définir une query de recherche pour les emplois à temps plein."""
        if query is None:
            embed = discord.Embed(
                title="⚠️ Erreur : Query manquante",
                description="Veuillez fournir une query pour définir une nouvelle valeur. Utilisez `!setqueryFulltime <query>`.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if not query.strip():
            embed = discord.Embed(
                title="⚠️ Erreur : Query vide",
                description="La query que vous avez fournie est vide. Veuillez entrer une query valide.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if query.strip() == "default":
            # Réinitialiser la query à la valeur par défaut
            self.query_fulltime = "Développeur full stack en France"  # Mettre une valeur par défaut appropriée
            env_path = Path('.') / '.env'
            set_key(env_path, 'QUERY_FULLTIME', self.query_fulltime)

            embed = discord.Embed(
                title="🔄 Query Réinitialisée",
                description=f"La query a été réinitialisée à : **{self.query_fulltime}**",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return

        if query == self.query_fulltime:
            embed = discord.Embed(
                title="⚠️ Query Identique",
                description="La query que vous avez fournie est identique à la query actuelle. Veuillez fournir une nouvelle query.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if len(query) > 100:
            embed = discord.Embed(
                title="⚠️ Query Trop Longue",
                description="La query que vous avez fournie est trop longue. Veuillez fournir une query de 100 caractères ou moins.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Mettre à jour la variable et le fichier .env
        self.query_fulltime = query
        env_path = Path('.') / '.env'
        set_key(env_path, 'QUERY_FULLTIME', query)

        embed = discord.Embed(
            title="✅ Query Initialisée",
            description=f"La query a été définie comme : **{self.query_fulltime}**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name='update_fulltime', aliases=['update_cdi'], description="Force la mise à jour des offres d'emploi pour les CDI.")
    async def update_cdi(self, ctx):
        """Force la mise à jour des offres d'emploi pour les CDI."""
        embed_loading = discord.Embed(
            title="🔄 Mise à Jour en Cours",
            description="La liste des offres d'emploi pour les CDI est en cours de mise à jour, veuillez patienter...",
            color=discord.Color.orange()
        )
        embed_loading.set_thumbnail(
            url="https://i.imgur.com/5AGlfwy.gif"
        )  # Lien vers une icône d'engrenage animée
        embed_loading.set_footer(text="unique_identifier")
        loading_message = await ctx.send(embed=embed_loading)

        await send_cdilist(self.bot, ctx, loading_message)

    @commands.command(name='update_internships', aliases=['update_jobs'],
                      description="Force la mise à jour des offres d'emploi pour les alternances.")
    async def update_job(self, ctx):
        """Force la mise à jour des offres d'emploi pour les alternances."""
        embed_loading = discord.Embed(
            title="🔄 Mise à Jour en Cours",
            description="La liste des offres d'emploi pour l'alternance est en cours de mise à jour. Veuillez patienter...",
            color=discord.Color.orange()
        )
        embed_loading.set_thumbnail(
            url="https://i.imgur.com/5AGlfwy.gif"  # Lien vers une icône d'engrenage animée
        )
        embed_loading.set_footer(text="unique_identifier")
        loading_message = await ctx.send(embed=embed_loading)

        await send_jobslist(self.bot, ctx, loading_message)

async def setup(bot):
    await bot.add_cog(Administration(bot))
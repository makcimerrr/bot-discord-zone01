import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import set_key, load_dotenv

from utils.config_loader import forbidden_words
from utils.utils_fulltime import send_cdilist
from utils.utils_function import is_admin
from utils.utils_internship import send_jobslist


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv(override=True)
        self.query_intern = os.getenv('QUERY_INTERNSHIP')  # Initialiser avec la variable depuis .env
        self.query_fulltime = os.getenv('QUERY_FULLTIME')  # Ajouter la variable pour fulltime
        self.forbidden_words = forbidden_words
        self.send_jobslist = send_jobslist
        self.send_cdilist = send_cdilist

    @commands.command(name='setqueryIntern')
    @is_admin()
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
    @is_admin()
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
    @is_admin()
    async def update_cdi(self, ctx):
        """Force la mise à jour des offres d'emploi pour les CDI."""
        embed_loading = discord.Embed(
            title="🔄 Mise à Jour en Cours",
            description="La liste des offres d'emploi pour les CDI est en cours de mise à jour, veuillez patienter...",
            color=discord.Color.orange()
        )
        embed_loading.add_field(name="Query :", value=self.query_fulltime, inline=False)
        embed_loading.set_thumbnail(
            url="https://i.imgur.com/5AGlfwy.gif"
        )  # Lien vers une icône d'engrenage animée
        embed_loading.set_footer(text="unique_identifier")
        loading_message = await ctx.send(embed=embed_loading)

        await send_cdilist(self.bot, ctx, loading_message)

    @commands.command(name='update_internships', aliases=['update_jobs'],
                      description="Force la mise à jour des offres d'emploi pour les alternances.")
    @is_admin()
    async def update_job(self, ctx):
        """Force la mise à jour des offres d'emploi pour les alternances."""
        embed_loading = discord.Embed(
            title="🔄 Mise à Jour en Cours",
            description="La liste des offres d'emploi pour l'alternance est en cours de mise à jour. Veuillez patienter...",
            color=discord.Color.orange()
        )
        embed_loading.add_field(name="Query :", value=self.query_intern, inline=False)
        embed_loading.set_thumbnail(
            url="https://i.imgur.com/5AGlfwy.gif"  # Lien vers une icône d'engrenage animée
        )
        embed_loading.set_footer(text="unique_identifier")
        loading_message = await ctx.send(embed=embed_loading)

        await send_jobslist(self.bot, ctx, loading_message)

async def setup(bot):
    await bot.add_cog(Administration(bot))
import os
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv, set_key

from utils.config_loader import forbidden_words
from utils.utils_fulltime import send_cdilist
from utils.utils_function import is_admin
from utils.utils_internship import send_jobslist

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        env_path = Path('../.env')  # Charger le fichier .env situé à la racine du projet
        load_dotenv(dotenv_path=env_path, override=True)

        self.query_intern = os.getenv('QUERY_INTERNSHIP')  # Récupérer la query depuis .env
        self.query_fulltime = os.getenv('QUERY_FULLTIME')  # Récupérer la query fulltime depuis .env
        self.forbidden_words = forbidden_words
        self.send_jobslist = send_jobslist
        self.send_cdilist = send_cdilist

    def update_env_key(self, key, value):
        """ Fonction utilitaire pour mettre à jour ou ajouter une clé dans le fichier .env """
        env_path = Path('../.env')  # Chemin du fichier .env
        current_value = os.getenv(key)  # Récupérer la valeur actuelle

        if current_value is None or current_value.strip() != value.strip():
            set_key(env_path, key, value)  # Mettre à jour ou créer la clé dans .env
            return True
        return False

    @commands.command(name='setqueryIntern')
    @is_admin()
    async def set_query_intern(self, ctx, query: str = None):
        """Commande pour définir ou mettre à jour la query de recherche pour les alternances."""
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
            self.query_intern = "Alternance Développeur Rouen"  # Valeur par défaut
            if self.update_env_key('QUERY_INTERNSHIP', self.query_intern):
                embed = discord.Embed(
                    title="🔄 Query Réinitialisée",
                    description=f"La query a été réinitialisée à : **{self.query_intern}**",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="⚠️ Aucune modification",
                    description="La query est déjà définie à cette valeur.",
                    color=discord.Color.red()
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
        if self.update_env_key('QUERY_INTERNSHIP', query):
            embed = discord.Embed(
                title="✅ Query Initialisée",
                description=f"La query a été définie comme : **{self.query_intern}**",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="⚠️ Aucune modification",
                description="La query est déjà définie à cette valeur.",
                color=discord.Color.red()
            )

        await ctx.send(embed=embed)

    @commands.command(name='setqueryFulltime')
    @is_admin()
    async def set_query_fulltime(self, ctx, query: str = None):
        """Commande pour définir ou mettre à jour la query de recherche pour les emplois à temps plein."""
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
            self.query_fulltime = "Développeur full stack en France"  # Valeur par défaut
            if self.update_env_key('QUERY_FULLTIME', self.query_fulltime):
                embed = discord.Embed(
                    title="🔄 Query Réinitialisée",
                    description=f"La query a été réinitialisée à : **{self.query_fulltime}**",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="⚠️ Aucune modification",
                    description="La query est déjà définie à cette valeur.",
                    color=discord.Color.red()
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
        if self.update_env_key('QUERY_FULLTIME', query):
            embed = discord.Embed(
                title="✅ Query Initialisée",
                description=f"La query a été définie comme : **{self.query_fulltime}**",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="⚠️ Aucune modification",
                description="La query est déjà définie à cette valeur.",
                color=discord.Color.red()
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Administration(bot))
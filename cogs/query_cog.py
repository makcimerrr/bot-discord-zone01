import discord
from discord.ext import commands
from utils.config_loader import query_intern, query_fulltime
from dotenv import set_key
from pathlib import Path

class QueryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.query_intern = query_intern  # Initialiser avec la variable depuis .env
        self.query_fulltime = query_fulltime  # Ajouter la variable pour fulltime

    @commands.command(name='setqueryIntern')
    async def set_query_intern(self, ctx, query: str = None):
        """Commande pour définir une query pour les stages."""
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
            self.query_intern = "Développeur full stack en France"  # Mettre une valeur par défaut appropriée
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

    @commands.command(name='showqueryIntern')
    async def show_query_intern(self, ctx):
        """Commande pour afficher la query actuelle pour les stages."""
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

    @commands.command(name='setqueryFulltime')
    async def set_query_fulltime(self, ctx, query: str = None):
        """Commande pour définir une query pour les emplois à temps plein."""
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
            self.query_fulltime = "Développeur web senior en France"  # Mettre une valeur par défaut appropriée
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

    def get_query_intern(self):
        """Renvoie la valeur actuelle de query_intern."""
        return self.query_intern

    def get_query_fulltime(self):
        """Renvoie la valeur actuelle de query_fulltime."""
        return self.query_fulltime

# Fonction pour ajouter le Cog au bot
async def setup(bot):
    await bot.add_cog(QueryCog(bot))

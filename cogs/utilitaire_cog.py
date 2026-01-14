import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from utils.logger import logger


class Utilitaire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', aliases=['pingme', 'pingpong', 'pingtest', 'latence', 'latency'],
                      description="Renvoie la latence du bot en millisecondes.")
    async def ping(self, ctx):
        """Renvoie la latence du bot en millisecondes."""
        await ctx.send(f"🏓 Pong ! `{round(self.bot.latency * 1000)}ms` <@!{ctx.author.id}>")

    @app_commands.command(name="bot_logs", description="Affiche les logs généraux du bot")
    @app_commands.describe(
        limit="Nombre de logs à afficher (par défaut: 20, max: 50)",
        level="Filtrer par niveau (ERROR, WARNING, INFO, SUCCESS, DEBUG)",
        category="Filtrer par catégorie (bot, notion, config, general)"
    )
    @app_commands.choices(level=[
        app_commands.Choice(name="Tous", value="all"),
        app_commands.Choice(name="ERROR", value="ERROR"),
        app_commands.Choice(name="WARNING", value="WARNING"),
        app_commands.Choice(name="INFO", value="INFO"),
        app_commands.Choice(name="SUCCESS", value="SUCCESS"),
    ])
    @app_commands.choices(category=[
        app_commands.Choice(name="Toutes", value="all"),
        app_commands.Choice(name="Bot", value="bot"),
        app_commands.Choice(name="Notion", value="notion"),
        app_commands.Choice(name="Config", value="config"),
        app_commands.Choice(name="General", value="general"),
    ])
    async def bot_logs_command(
        self,
        interaction: discord.Interaction,
        limit: int = 20,
        level: app_commands.Choice[str] = None,
        category: app_commands.Choice[str] = None
    ):
        """Affiche les logs généraux du bot"""
        await interaction.response.defer(ephemeral=True)

        limit = min(max(1, limit), 50)

        level_filter = level.value if level and level.value != "all" else None
        category_filter = category.value if category and category.value != "all" else None

        logs = logger.get_logs(limit=limit, level=level_filter, category=category_filter)

        if not logs:
            await interaction.followup.send("Aucun log trouvé.", ephemeral=True)
            return

        stats = logger.get_stats()

        embed = discord.Embed(
            title="📋 Logs du Bot",
            description=f"Affichage des {len(logs)} derniers logs",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )

        embed.add_field(
            name="📊 Statistiques globales",
            value=f"✅ Success: {stats['success']} | ℹ️ Info: {stats['info']} | ⚠️ Warning: {stats['warning']} | ❌ Error: {stats['error']}",
            inline=False
        )

        level_icons = {
            "ERROR": "❌",
            "WARNING": "⚠️",
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "DEBUG": "🔧"
        }

        logs_text = []
        for log in logs:
            try:
                timestamp = datetime.fromisoformat(log['timestamp'])
                formatted_time = timestamp.strftime("%d/%m %H:%M")
            except:
                formatted_time = "??/?? ??:??"

            icon = level_icons.get(log['level'], "📝")
            cat = f"[{log['category']}]" if log['category'] != "general" else ""
            message = log['message'][:80] + "..." if len(log['message']) > 80 else log['message']
            logs_text.append(f"`{formatted_time}` {icon} {cat} {message}")

        chunk_size = 10
        for i in range(0, len(logs_text), chunk_size):
            chunk = logs_text[i:i + chunk_size]
            field_name = "📜 Logs récents" if i == 0 else "​"
            embed.add_field(name=field_name, value="\n".join(chunk), inline=False)

        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utilitaire(bot))

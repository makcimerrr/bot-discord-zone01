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

    @app_commands.command(name="logs", description="Affiche les logs généraux du bot")
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
    async def logs_command(
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

    @app_commands.command(name="logs_clear", description="Efface tous les logs du bot")
    @app_commands.default_permissions(administrator=True)
    async def logs_clear_command(self, interaction: discord.Interaction):
        """Efface tous les logs du bot"""
        stats = logger.get_stats()
        total = stats['total']

        if total == 0:
            await interaction.response.send_message("Les logs sont déjà vides.", ephemeral=True)
            return

        logger.clear_logs()
        logger.info(f"Logs effacés par {interaction.user.name}", category="bot")

        await interaction.response.send_message(
            f"🗑️ **{total} logs** ont été effacés.",
            ephemeral=True
        )

    @app_commands.command(name="logs_stats", description="Affiche les statistiques détaillées des logs")
    async def logs_stats_command(self, interaction: discord.Interaction):
        """Affiche les statistiques détaillées des logs"""
        stats = logger.get_stats()
        all_logs = logger.get_logs(limit=500)

        embed = discord.Embed(
            title="📊 Statistiques des Logs",
            color=discord.Color.gold(),
            timestamp=datetime.now()
        )

        embed.add_field(
            name="📈 Total",
            value=f"**{stats['total']}** logs enregistrés",
            inline=False
        )

        stats_text = (
            f"✅ Success: **{stats['success']}** ({self._percent(stats['success'], stats['total'])})\n"
            f"ℹ️ Info: **{stats['info']}** ({self._percent(stats['info'], stats['total'])})\n"
            f"⚠️ Warning: **{stats['warning']}** ({self._percent(stats['warning'], stats['total'])})\n"
            f"❌ Error: **{stats['error']}** ({self._percent(stats['error'], stats['total'])})\n"
            f"🔧 Debug: **{stats['debug']}** ({self._percent(stats['debug'], stats['total'])})"
        )
        embed.add_field(name="📋 Par niveau", value=stats_text, inline=True)

        categories = {}
        for log in all_logs:
            cat = log.get('category', 'general')
            categories[cat] = categories.get(cat, 0) + 1

        if categories:
            cat_text = "\n".join([f"**{cat}**: {count}" for cat, count in sorted(categories.items(), key=lambda x: -x[1])])
            embed.add_field(name="🏷️ Par catégorie", value=cat_text, inline=True)

        if all_logs:
            try:
                first_log = min(all_logs, key=lambda x: x['timestamp'])
                last_log = max(all_logs, key=lambda x: x['timestamp'])
                first_time = datetime.fromisoformat(first_log['timestamp']).strftime("%d/%m/%Y %H:%M")
                last_time = datetime.fromisoformat(last_log['timestamp']).strftime("%d/%m/%Y %H:%M")
                embed.add_field(
                    name="🕐 Période",
                    value=f"Du **{first_time}**\nAu **{last_time}**",
                    inline=False
                )
            except:
                pass

        errors = [log for log in all_logs if log['level'] == 'ERROR'][-5:]
        if errors:
            error_text = []
            for err in reversed(errors):
                try:
                    timestamp = datetime.fromisoformat(err['timestamp']).strftime("%d/%m %H:%M")
                except:
                    timestamp = "??/??"
                msg = err['message'][:60] + "..." if len(err['message']) > 60 else err['message']
                error_text.append(f"`{timestamp}` {msg}")
            embed.add_field(name="❌ Dernières erreurs", value="\n".join(error_text), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="logs_export", description="Exporte les logs en fichier texte")
    @app_commands.describe(
        level="Filtrer par niveau",
        category="Filtrer par catégorie"
    )
    @app_commands.choices(level=[
        app_commands.Choice(name="Tous", value="all"),
        app_commands.Choice(name="ERROR", value="ERROR"),
        app_commands.Choice(name="WARNING", value="WARNING"),
    ])
    async def logs_export_command(
        self,
        interaction: discord.Interaction,
        level: app_commands.Choice[str] = None,
        category: str = None
    ):
        """Exporte les logs en fichier texte"""
        await interaction.response.defer(ephemeral=True)

        level_filter = level.value if level and level.value != "all" else None
        category_filter = category if category else None

        logs = logger.get_logs(limit=500, level=level_filter, category=category_filter)

        if not logs:
            await interaction.followup.send("Aucun log à exporter.", ephemeral=True)
            return

        lines = []
        for log in reversed(logs):
            lines.append(f"[{log['timestamp']}] [{log['level']}] [{log['category']}] {log['message']}")

        content = "\n".join(lines)

        filename = f"logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file = discord.File(fp=__import__('io').StringIO(content), filename=filename)

        filter_info = []
        if level_filter:
            filter_info.append(f"niveau={level_filter}")
        if category_filter:
            filter_info.append(f"catégorie={category_filter}")
        filter_text = f" (filtres: {', '.join(filter_info)})" if filter_info else ""

        await interaction.followup.send(
            f"📄 Export de **{len(logs)}** logs{filter_text}",
            file=file,
            ephemeral=True
        )

    def _percent(self, value, total):
        """Calcule le pourcentage"""
        if total == 0:
            return "0%"
        return f"{round(value / total * 100)}%"

async def setup(bot):
    await bot.add_cog(Utilitaire(bot))

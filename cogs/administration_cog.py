import os
from pathlib import Path
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv, set_key

from utils.config_loader import forbidden_words
from utils.utils_fulltime import send_cdilist
from utils.utils_function import is_admin, is_admin_slash
from utils.utils_internship import send_jobslist
from utils.timeline import fetch_and_send_progress

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

    @commands.command(name='timeline', aliases=['tl'], description="Affiche la timeline des promotions.")
    @is_admin()
    async def timeline(self, ctx):
        await fetch_and_send_progress(self.bot)

    @app_commands.command(name="timeline", description="Met à jour la progression des promotions avec suivi en temps réel")
    @is_admin_slash()
    async def timeline_slash(self, interaction: discord.Interaction):
        """Met à jour la progression de toutes les promotions avec suivi en temps réel"""
        from utils.progress_fetcher import fetch_progress
        from utils.config_loader import config
        import re
        from datetime import datetime

        # Message initial
        embed = discord.Embed(
            title="⏳ Mise à jour en cours...",
            description="Récupération des données de progression...",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Récupération des données
        progress_data = await fetch_progress()

        if not progress_data:
            embed_error = discord.Embed(
                title="❌ Erreur",
                description="Impossible de récupérer les données de progression pour le moment.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            )
            await interaction.edit_original_response(embed=embed_error)
            return

        # Mise à jour : traitement en cours
        total_promos = len(progress_data)
        embed_processing = discord.Embed(
            title="🔄 Traitement en cours...",
            description=f"Traitement de {total_promos} promotion(s)...",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        await interaction.edit_original_response(embed=embed_processing)

        # Traitement de chaque promotion
        success_count = 0
        error_count = 0
        errors = []

        for idx, item in enumerate(progress_data, 1):
            # Mise à jour de la progression
            embed_update = discord.Embed(
                title="🔄 Traitement en cours...",
                description=f"Traitement de la promotion **{item['promotionName']}** ({idx}/{total_promos})",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow()
            )
            embed_update.add_field(
                name="📊 Progression",
                value=f"`{idx}/{total_promos}` promotions traitées",
                inline=False
            )
            await interaction.edit_original_response(embed=embed_update)

            # Création de l'embed de progression
            progress_emoji = "🟩" * (item['progress'] // 10) + "🟥" * (10 - (item['progress'] // 10))

            embed_progress = discord.Embed(
                title=f"📚 Projet en cours : `{item.get('currentProject', 'Non spécifié')}`",
                description=f"👤 **Promotion** : `{item['promotionName']}`",
                color=discord.Color.green() if item['success'] else discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed_progress.set_author(name="Suivi de progression Zone01", icon_url="https://example.com/logo.png")
            embed_progress.add_field(
                name="📈 Progression",
                value=f"`{item['progress']}%`  \n{progress_emoji}",
                inline=True
            )

            # Extraction de la date
            agenda_str = item.get('agenda', ['Non spécifié'])[0]
            match = re.search(r"(Fin de la promo:|Fin du projet actuel :)\s*(\d{4}-\d{2}-\d{2})", agenda_str)

            if match:
                date_str = match.group(2)
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    formatted_date = f"Le {date_obj.day} {date_obj.strftime('%B')} {date_obj.year}"
                except ValueError:
                    formatted_date = 'Non spécifié'
            else:
                formatted_date = 'Non spécifié'

            embed_progress.add_field(
                name="⏳ Échéance estimée",
                value=f"`{formatted_date}`",
                inline=True
            )

            if 'notes' in item and item['notes']:
                embed_progress.add_field(
                    name="📝 **Notes supplémentaires**",
                    value=item['notes'],
                    inline=False
                )

            embed_progress.set_footer(text="Zone01 Normandie • Mise à jour automatique", icon_url="https://example.com/footer-icon.png")

            # Envoi dans le canal approprié
            channel_name = f"channel_progress_{item['promotionName'].replace(' ', '_')}"
            channel_id = config.get(channel_name)

            channel_modo_id = 1257310056546963479
            channel_modo = self.bot.get_channel(channel_modo_id)

            if channel_id:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    # Supprimer les anciens messages
                    async for message in channel.history(limit=100):
                        if message.author == self.bot.user:
                            await message.delete()
                    # Envoi de l'embed
                    await channel.send(embed=embed_progress)
                    success_count += 1
                else:
                    error_count += 1
                    errors.append(f"❌ {item['promotionName']}: Canal ID `{channel_id}` non trouvé")
                    # Envoi erreur au canal modo
                    if channel_modo:
                        embed_error = discord.Embed(
                            title="🚫 Erreur Automatique",
                            description=f"Salon avec l'ID {channel_id} pour la promotion {item['promotionName']} non trouvé.",
                            color=discord.Color.red()
                        )
                        await channel_modo.send(embed=embed_error)
            else:
                error_count += 1
                errors.append(f"❌ {item['promotionName']}: Canal non configuré")
                # Envoi erreur au canal modo
                if channel_modo:
                    embed_error = discord.Embed(
                        title="🚫 Erreur Automatique",
                        description=f"Channel non configuré pour la promotion {item['promotionName']}.",
                        color=discord.Color.red()
                    )
                    await channel_modo.send(embed=embed_error)

        # Message final
        if error_count == 0:
            embed_final = discord.Embed(
                title="✅ Mise à jour terminée",
                description=f"Toutes les promotions ont été mises à jour avec succès !",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )
            embed_final.add_field(
                name="📊 Résumé",
                value=f"✅ **{success_count}** promotion(s) mise(s) à jour\n❌ **{error_count}** erreur(s)",
                inline=False
            )
        else:
            embed_final = discord.Embed(
                title="⚠️ Mise à jour terminée avec des erreurs",
                description=f"Certaines promotions n'ont pas pu être mises à jour.",
                color=discord.Color.orange(),
                timestamp=discord.utils.utcnow()
            )
            embed_final.add_field(
                name="📊 Résumé",
                value=f"✅ **{success_count}** promotion(s) mise(s) à jour\n❌ **{error_count}** erreur(s)",
                inline=False
            )
            if errors:
                embed_final.add_field(
                    name="🚨 Erreurs",
                    value="\n".join(errors[:10]),  # Limiter à 10 erreurs
                    inline=False
                )

        await interaction.edit_original_response(embed=embed_final)

async def setup(bot):
    await bot.add_cog(Administration(bot))
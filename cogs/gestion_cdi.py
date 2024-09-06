import discord
import re
from discord.ext import commands
import asyncio

from utils.config_loader import role_ping_cdi, forum_channel_id_cdi, guild_id
from utils.cdi_fetcher import fetch_api_fulltime

class CDICog(commands.Cog):
    """Cog pour la gestion des offres d'emploi CDI."""

    def __init__(self, bot):
        self.bot = bot

    async def send_cdilist(self, ctx=None, loading_message=None):

        if ctx:
            guild = ctx.guild
            forum_channel_cdi = guild.get_channel(forum_channel_id_cdi)
        else:
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                print("Guild not found")
                return
            forum_channel_cdi = guild.get_channel(forum_channel_id_cdi)

        if isinstance(forum_channel_cdi, discord.ForumChannel):
            # Obtenir les threads actifs et archivés existants
            active_threads = forum_channel_cdi.threads
            archived_threads = [
                thread
                async for thread in forum_channel_cdi.archived_threads(limit=100)
            ]

            all_threads = active_threads + archived_threads

            list_jobs, query_message = await fetch_api_fulltime(self.bot)

            # Vérification si aucune query n'a été initialisée
            if "Aucune query n'a été définie" in query_message:
                if ctx:
                    if loading_message:
                        embed_error = discord.Embed(
                            title="🚫 Erreur : Query Non Initialisée",
                            description="Aucune query n'a été définie. Veuillez initialiser une query avec `!setqueryFulltime`.",
                            color=discord.Color.red()
                        )
                        embed_error.set_footer(text="Veuillez configurer une query pour continuer.")
                        await loading_message.edit(embed=embed_error)
                        return  # Arrêter la fonction si la query n'est pas définie
                else:
                    channel_id = 1257310056546963479  # Remplace par l'ID de ton channel
                    channel = self.bot.get_channel(channel_id)
                    if channel:
                        embed_error = discord.Embed(
                            title="⚠️ Erreur Automatique",
                            description="La tâche automatique n'a pas pu s'exécuter car aucune query n'a été définie. Veuillez configurer une query avec `!setqueryFulltime`.",
                            color=discord.Color.red()
                        )
                        await channel.send(embed=embed_error)
                        return

            await asyncio.sleep(1)

            verif = False

            if ctx:
                if not list_jobs:
                    embed_no_jobs = discord.Embed(
                        title="🔍 Aucune Nouvelle Offre",
                        description="Aucune nouvelle offre d'emploi pour les contrats à temps plein n'a été trouvée.",
                        color=discord.Color.greyple()
                    )
                    embed_no_jobs.set_footer(text="Vérifiez plus tard pour les nouvelles offres.")
                    await ctx.send(embed=embed_no_jobs)
                    verif = True

                if verif:
                    if loading_message:
                        embed_updated = discord.Embed(
                            title="⚠️ Erreur lors de la Mise à Jour",
                            description="Aucune des listes d'offres d'emploi n'a pu être mise à jour. Veuillez réessayer plus tard.",
                            color=discord.Color.red()
                        )
                        embed_updated.add_field(
                            name="Message de l'API",
                            value=query_message if query_message else "Aucune query n'a été définie.",
                            inline=False
                        )
                        await loading_message.edit(embed=embed_updated)
                    return

            all_jobs = list_jobs
            found_threads = []
            new_threads_created = False

            for job in all_jobs:
                title = job.get("job_title")
                company = job.get("employer_name")
                date = job.get("job_posted_at_datetime_utc")
                link = job.get("job_apply_link")
                city = job.get("job_city")
                if not city:
                    city = job.get("job_state")

                if title and link and company:
                    thread_title = f"{company} - {title}"
                    if date and link:
                        thread_content = (
                            f"👋 Bonjour <@&{role_ping_cdi}> !\n\n"
                            f"🔎 Offre sur **{city}** chez **{company}**.\n"
                            f"📈 Poste recherché : **{title}**\n"
                            f"🔗 Pour plus de détails et pour postuler, cliquez sur le lien : [Postuler]({link})"
                        )

                        # Chercher un thread existant avec le même titre
                        existing_thread = None
                        for thread in all_threads:
                            if thread.name == thread_title:
                                existing_thread = thread
                                found_threads.append(existing_thread)
                                break

                        # Si un thread avec le même titre existe déjà, passe au suivant
                        if existing_thread:
                            print("Thread trouvé :", existing_thread.name)
                            continue

                        # Créer le nouveau thread
                        try:
                            thread = await forum_channel_cdi.create_thread(
                                name=thread_title, content=thread_content)
                            new_threads_created = True
                            await asyncio.sleep(1)
                        except discord.errors.HTTPException as e:
                            if e.code == 429:
                                print("Rate limited by Discord, retrying later.")
                                break

                        await asyncio.sleep(1)

            # Vérifier si aucun nouveau thread n'a été créé
            if not new_threads_created:
                if loading_message:
                    embed_updated = discord.Embed(
                        title="🔔 Aucune Nouvelle Offre",
                        description="Aucune nouvelle offre d'emploi n'a été trouvée pour les CDI.",
                        color=discord.Color.green()
                    )
                    embed_updated.add_field(
                        name="Message de l'API",
                        value=query_message if query_message else "Aucune query n'a été définie.",
                        inline=False
                    )
                    await loading_message.edit(embed=embed_updated)
            else:
                if loading_message:
                    embed_updated = discord.Embed(
                        title="✅ Mise à Jour Complète",
                        description="Toutes les nouvelles offres d'emploi ont été publiées avec succès.",
                        color=discord.Color.blue()
                    )
                    embed_updated.add_field(
                        name="Message de l'API",
                        value=query_message if query_message else "Aucune query n'a été définie.",
                        inline=False
                    )
                    await loading_message.edit(embed=embed_updated)

        else:
            print("Le canal spécifié n'est pas un ForumChannel.")
            if loading_message:
                embed_updated = discord.Embed(
                    title="❌ Erreur de Canal",
                    description="Le canal spécifié n'est pas un ForumChannel.",
                    color=discord.Color.red()
                )
                await loading_message.edit(embed=embed_updated)

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
        loading_message = await ctx.send(embed=embed_loading)

        await self.send_cdilist(ctx, loading_message)


async def setup(bot):
    await bot.add_cog(CDICog(bot))

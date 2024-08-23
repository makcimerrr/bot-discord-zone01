import re
import discord
from discord.ext import commands
import asyncio

from utils.config_loader import forum_channel_id, role_ping, guild_id, role_p1_2023, role_p2_2023
from utils.intern_fetcher import fetch_api_intern


class JobCog(commands.Cog):
    """Cog pour la gestion des offres d'emploi."""

    def __init__(self, bot):
        self.bot = bot

    async def send_joblist(self, ctx=None, loading_message=None):

        # forum_channel = ctx.guild.get_channel(forum_channel_id)

        if ctx:
            guild = ctx.guild
            forum_channel = guild.get_channel(forum_channel_id)
        else:
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                print("Guild not found")
                return
            forum_channel = guild.get_channel(forum_channel_id)

        if isinstance(forum_channel, discord.ForumChannel):
            # Obtenir les threads actifs et archivés existants
            active_threads = forum_channel.threads
            archived_threads = [
                thread
                async for thread in forum_channel.archived_threads(limit=100)
            ]

            all_threads = active_threads + archived_threads

            # Récupérer les offres d'emploi depuis les API
            intern_jobs = await fetch_api_intern()
            await asyncio.sleep(1)
            verif = False

            if ctx:
                if not intern_jobs:
                    await ctx.send("Erreur lors de la récupération des offres d'emploi pour les alternants.")
                    verif = True

                if verif:
                    if loading_message:
                        # Modifier l'embed de chargement pour indiquer la fin de la mise à jour
                        embed_updated = discord.Embed(
                            title="Erreur lors de la mise à jour",
                            description=f"Aucune des listes d'offres d'emploi n'a pu être mise à jour. Veuillez "
                                        f"réessayer plus tard.",
                            color=discord.Color.red()
                        )
                        await loading_message.edit(embed=embed_updated)
                    return

            # Fusionner les deux listes d'offres d'emploi
            all_jobs = intern_jobs

            found_threads = []
            new_threads_created = False

            for job in all_jobs:

                title = job.get("job_title")
                company = job.get("employer_name")
                date = job.get("job_posted_at_datetime_utc")
                link = job.get("job_apply_link")
                city = job.get("job_city")
                technologies = job.get("job_technologies")

                if title and link and company:
                    thread_title = f"{company} - {title}"

                    if date and link:
                        thread_content = f"Bonjour <@&{role_p1_2023}> et <@&{role_p2_2023}> ! Offre d'alternance sur **{city}**, chez **{company}** qui recherche un développeur **{title}** utilisant les technologies suivantes : **{technologies}**. Pour plus de détails et pour postuler, cliquez sur le lien : {link}"

                        # Chercher un thread existant avec le même titre
                        existing_thread = None
                        for thread in all_threads:
                            if thread.name == thread_title:
                                existing_thread = thread
                                found_threads.append(existing_thread)
                                break

                        # Si un thread avec le même titre existe déjà, passe au suivant
                        if existing_thread:
                            print("Thread found:", existing_thread.name)
                            continue

                        # Créer le nouveau thread
                        try:
                            thread = await forum_channel.create_thread(
                                name=thread_title, content=thread_content)
                            new_threads_created = True
                        except discord.errors.HTTPException as e:
                            if e.code == 429:
                                print(
                                    "Rate limited by Discord, will try again later."
                                )
                                break

                        await asyncio.sleep(1)
            # Vérifier si aucun nouveau thread n'a été créé
            if not new_threads_created:
                if loading_message:
                    embed_updated = discord.Embed(
                        title="Aucune nouvelle offre",
                        description="Aucune nouvelle offre d'emploi n'a été trouvée.",
                        color=discord.Color.green()
                    )
                    await loading_message.edit(embed=embed_updated)
            else:
                if loading_message:
                    embed_updated = discord.Embed(
                        title="Mise à jour terminée",
                        description="Toutes les nouvelles offres d'emploi ont été publiées avec succès.",
                        color=discord.Color.blue()
                    )
                    await loading_message.edit(embed=embed_updated)


        else:
            print("Le canal spécifié n'est pas un ForumChannel.")
            if loading_message:
                embed_updated = discord.Embed(
                    title="Erreur lors de la mise à jour",
                    description="Le canal spécifié n'est pas un ForumChannel.",
                    color=discord.Color.red()
                )
                await loading_message.edit(embed=embed_updated)

    @commands.command(name='update_jobs')
    async def update_jobs(self, ctx):
        """Force la mise à jour des offres d'emploi pour les alternants."""
        # await ctx.send(f"Updated jobs list !")
        embed_loading = discord.Embed(
            title="Mise à jour en cours",
            description="La liste des offres d'emploi pour les alternants est en cours de mise à jour, veuillez "
                        "patienter...",
            color=discord.Color.orange()
        )
        embed_loading.set_thumbnail(
            url="https://i.imgur.com/5AGlfwy.gif")  # Lien vers une icône d'engrenage animée
        loading_message = await ctx.send(embed=embed_loading)

        await self.send_joblist(ctx, loading_message)
        # await ctx.send(f"Fini !")


async def setup(bot):
    await bot.add_cog(JobCog(bot))

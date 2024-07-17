import discord
from discord.ext import commands
import asyncio

from utils.config_loader import forum_channel_id
from utils.job_fetcher import fetch_linkedin_jobs, fetch_indeed_jobs, fetch_new_jobs


class JobCog(commands.Cog):
    """Cog pour la gestion des offres d'emploi."""

    def __init__(self, bot):
        self.bot = bot

    async def send_joblist(self, ctx=None, loading_message=None):
        forum_channel = self.bot.get_channel(forum_channel_id)

        if isinstance(forum_channel, discord.ForumChannel):
            linkedin_jobs = fetch_linkedin_jobs()
            await asyncio.sleep(1)
            indeed_jobs = fetch_indeed_jobs()
            await asyncio.sleep(1)
            jSearch_jobs = fetch_new_jobs()
            await asyncio.sleep(1)

            bugs = []

            if ctx:
                if not linkedin_jobs:
                    bugs.append("Linkedin")
                if not indeed_jobs:
                    bugs.append("Indeed")
                if not jSearch_jobs:
                    bugs.append("JSearch")

                if bugs:
                    await ctx.send(
                        f"La liste des offres d'emploi de {bugs} n'a pas pu être mise à jour. Veuillez réessayer plus tard.")

            # Logique pour créer les threads d'offres d'emploi...

    @commands.command(name='update_jobs')
    async def update_jobs(self, ctx):
        """Force la mise à jour des offres d'emploi."""
        embed_loading = discord.Embed(
            title="Mise à jour en cours",
            description="La liste des offres d'emploi est en cours de mise à jour, veuillez patienter...",
            color=discord.Color.orange()
        )
        loading_message = await ctx.send(embed=embed_loading)
        await self.send_joblist(ctx, loading_message)


async def setup(bot):
    await bot.add_cog(JobCog(bot))

import discord
from discord.ext import commands


class Utilitaire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', aliases=['pingme', 'pingpong', 'pingtest', 'latence', 'latency'],
                      description="Renvoie la latence du bot en millisecondes.")
    async def ping(self, ctx):
        """Renvoie la latence du bot en millisecondes."""
        await ctx.send(f"🏓 Pong ! `{round(self.bot.latency * 1000)}ms` <@!{ctx.author.id}>")

async def setup(bot):
    await bot.add_cog(Utilitaire(bot))

from discord.ext import commands
from utils.config_loader import role_ping


class PingCog(commands.Cog):
    """Cog pour la commande ping."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Renvoie la latence du bot en millisecondes."""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms <@&{role_ping}>")


async def setup(bot):
    await bot.add_cog(PingCog(bot))

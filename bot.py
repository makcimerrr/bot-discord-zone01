from sched import scheduler
import discord
from discord.ext import commands, tasks

from cogs.gestion_help import SupremeHelpCommand
from utils.config_loader import config, discord_token, forum_channel_id, role_ping
from utils.scheduler import start_scheduler

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

initial_extensions = ['cogs.gestion_ping', 'cogs.gestion_jobs']


async def load_extensions(bot):
    for extension in initial_extensions:
        await bot.load_extension(extension)


@bot.event
async def on_ready():
    print('Bot is ready.')
    await load_extensions(bot)
    # Démarrage du scheduler pour exécuter la fonction send_joblist deux fois par jour
    start_scheduler()

attributes = {
    'name': "help",
    'aliases': ["helpme"],
    'cooldown': commands.CooldownMapping.from_cooldown(3, 5, commands.BucketType.user),
}

bot.help_command = SupremeHelpCommand(command_attrs=attributes)

bot.run(discord_token)

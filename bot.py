import asyncio
from sched import scheduler
import discord
import logging
from discord.ext import commands, tasks
from discord.ui import Modal, TextInput

from cogs.gestion_help import SupremeHelpCommand
from utils.config_loader import config, discord_token, forum_channel_id, role_ping
from utils.scheduler import start_scheduler

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

initial_extensions = ['cogs.gestion_ping', 'cogs.gestion_jobs', 'cogs.gestion_cdi', 'cogs.event_cog', 'cogs.helped_student', 'cogs.embed_cog']

# Flag to check if the bot is loading for the first time
first_ready = True


async def load_extensions(bot):
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            # print(f"Loaded {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")


@bot.event
async def on_ready():
    global first_ready
    print('Bot is ready.')

    if first_ready:
        await load_extensions(bot)
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)
        # Start the scheduler to run the send_joblist function twice a day
        start_scheduler(bot)
        first_ready = False


@bot.event
async def on_disconnect():
    logging.warning("Bot disconnected, attempting to reconnect...")
    print("Bot disconnected, attempting to reconnect...")


@bot.event
async def on_error(event, *args, **kwargs):
    logging.error(f"An error occurred in event {event}: {args[0]}")
    with open("err.log", "a") as f:
        f.write(f"Error in {event}: {args[0]}\n")


@bot.event
async def on_resumed():
    print("Bot reconnected.")


@bot.event
async def on_connect():
    print("Bot connected to Discord.")


@bot.event
async def on_close():
    print("Bot disconnected from Discord.")


attributes = {
    'name': "help",
    'aliases': ["helpme"],
    'cooldown': commands.CooldownMapping.from_cooldown(3, 5, commands.BucketType.user),
}

bot.help_command = SupremeHelpCommand(command_attrs=attributes)

bot.run(discord_token)

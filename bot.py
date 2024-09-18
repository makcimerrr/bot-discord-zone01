import asyncio
import traceback
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

initial_extensions = ['cogs.administration_cog', 'cogs.configuration_cog', 'cogs.utilitaire_cog']

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
        # Start the scheduler to run the send_joblist and send_cdilist function twice a day
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
async def on_message(message):
    try:
        # Your existing on_message code here
        await bot.process_commands(message)
    except Exception as e:
        logging.error(f"An error occurred in event on_message: {message}", exc_info=True)



@bot.event
async def on_resumed():
    print("Bot reconnected.")


@bot.event
async def on_connect():
    print("Bot connected to Discord.")


@bot.event
async def on_close():
    print("Bot disconnected from Discord.")


# Ajoutez ce gestionnaire d'erreurs globalement dans votre fichier principal
# Gestionnaire d'événements pour les erreurs globales
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="🚫 Commande Inconnue",
            description="La commande que vous avez essayée n'existe pas. Veuillez vérifier la commande et réessayer.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Utilisez !help pour voir les commandes disponibles.")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandInvokeError):
        # Gestion d'erreurs spécifiques
        tb = traceback.extract_tb(error.original.__traceback__)
        filename = tb[-1].filename
        line_number = tb[-1].lineno
        error_message = str(error)

        # Récupérer le dernier embed envoyé avec l'identifiant unique
        async for message in ctx.channel.history(limit=10):
            if message.embeds and message.embeds[0].footer.text == "unique_identifier":
                embed = message.embeds[0]

                # Modifier le dernier embed avec les nouvelles erreurs
                embed.title = "❌ Erreur d'Exécution"
                embed.description = "Une erreur s'est produite lors de l'exécution de la commande. Veuillez réessayer plus tard."
                embed.color=discord.Color.red()
                embed.set_thumbnail(url=None)
                embed.add_field(name="Erreur", value=error_message)
                embed.add_field(name="Fichier", value=filename)
                embed.add_field(name="Ligne", value=line_number)
                embed.add_field(name="Fonction", value=ctx.command.name)
                embed.set_footer(text="Veuillez vérifier et réessayer.")
                await message.edit(embed=embed)
                break
        else:
            # Si aucun embed n'est trouvé, créer un nouvel embed
            embed = discord.Embed(
                title="❌ Erreur d'Exécution",
                description="Une erreur s'est produite lors de l'exécution de la commande. Veuillez réessayer plus tard.",
                color=discord.Color.red()
            )
            embed.add_field(name="Erreur", value=error_message)
            embed.add_field(name="Fichier", value=filename)
            embed.add_field(name="Ligne", value=line_number)
            embed.add_field(name="Fonction", value=ctx.command.name)
            embed.set_footer(text="Veuillez vérifier et réessayer.")
            await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="🚫 Permissions Manquantes",
            description="Vous n'avez pas les permissions nécessaires pour exécuter cette commande.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ Erreur",
            description=str(error),
            color=discord.Color.red()
        )
        embed.set_footer(text="Veuillez vérifier la commande et réessayer.")
        await ctx.send(embed=embed)


attributes = {
    'name': "help",
    'aliases': ["helpme"],
    'cooldown': commands.CooldownMapping.from_cooldown(3, 5, commands.BucketType.user),
}

bot.help_command = SupremeHelpCommand(command_attrs=attributes)

bot.run(discord_token)

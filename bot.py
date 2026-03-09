import asyncio
import traceback
from sched import scheduler
import discord
import logging
from discord.ext import commands, tasks
from discord.ui import Modal, TextInput

from cogs.help_cog import SupremeHelpCommand
from utils.config_loader import config, discord_token, forum_channel_id, connect_base_url, connect_port
from utils.scheduler import start_scheduler
from utils.handlers import handle_dm
from utils.logger import logger
from utils.web_server import start_web_server

# Désactiver les logs Discord.py dans le terminal
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.getLogger('discord.http').setLevel(logging.CRITICAL)
logging.getLogger('discord.gateway').setLevel(logging.CRITICAL)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)
bot.connect_base_url = connect_base_url  # URL publique utilisée pour générer les liens /connect

initial_extensions = ['cogs.administration_cog', 'cogs.configuration_cog', 'cogs.utilitaire_cog', 'cogs.reaction_help_cog', 'cogs.connect_cog']

# Flag to check if the bot is loading for the first time
first_ready = True


async def load_extensions(bot):
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            logger.success(f"Extension chargée : {extension}", category="bot")
        except Exception as e:
            logger.error(f"Échec du chargement de l'extension {extension} : {e}", category="bot")


@bot.event
async def on_ready():
    global first_ready
    logger.success('Bot Discord démarré avec succès', category="bot")

    if first_ready:
        await load_extensions(bot)
        try:
            synced = await bot.tree.sync()
            logger.success(f"Synchronisation de {len(synced)} commande(s) slash", category="bot")
        except Exception as e:
            logger.error(f"Erreur lors de la synchronisation des commandes : {e}", category="bot")
        # Start the scheduler to run the send_joblist and send_cdilist function twice a day
        start_scheduler(bot)
        logger.info("Scheduler démarré pour les mises à jour automatiques", category="bot")
        # Start the web server for the OAuth2-like connect flow
        await start_web_server(bot, port=connect_port)
        first_ready = False


@bot.event
async def on_disconnect():
    logger.warning("Bot déconnecté, tentative de reconnexion...", category="bot")


@bot.event
async def on_error(event, *args, **kwargs):
    error_msg = f"Erreur dans l'événement {event}"
    if args:
        error_msg += f": {args[0]}"
    logger.error(error_msg, category="bot")


@bot.event
async def on_message(message):
    try:
        # Your existing on_message code here
        await bot.process_commands(message)
    except Exception as e:
        logger.error(f"Erreur dans on_message : {e}", category="bot")


@bot.event
async def on_resumed():
    logger.success("Bot reconnecté à Discord", category="bot")


@bot.event
async def on_connect():
    logger.success("Bot connecté à Discord", category="bot")


@bot.event
async def on_close():
    logger.warning("Bot déconnecté de Discord", category="bot")


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
                embed.color = discord.Color.red()
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

@bot.event
async def on_message(message):
    await handle_dm(bot, message)
    await bot.process_commands(message)


attributes = {
    'name': "help",
    'aliases': ["helpme"],
    'cooldown': commands.CooldownMapping.from_cooldown(3, 5, commands.BucketType.user),
}

bot.help_command = SupremeHelpCommand(command_attrs=attributes)

bot.run(discord_token)

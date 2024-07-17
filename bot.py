from sched import scheduler
import discord
from discord.ext import commands, tasks

from cogs.gestion_help import SupremeHelpCommand
from utils.config_loader import config, discord_token, forum_channel_id, role_ping
from utils.scheduler import start_scheduler

# Initialisation des intents pour le bot Discord
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

# Création du bot avec un préfixe de commande
bot = commands.Bot(command_prefix="!", intents=intents)

# Extensions initiales à charger
initial_extensions = ['cogs.gestion_ping', 'cogs.gestion_jobs', 'cogs.gestion_cdi']


async def load_extensions(bot):
    """
    Charge les extensions spécifiées pour le bot.

    Parameters
    ----------
    bot : commands.Bot
        L'instance du bot Discord pour laquelle les extensions doivent être chargées.

    Raises
    ------
    ExtensionNotFound
        Si une extension spécifiée ne peut pas être trouvée.
    """
    for extension in initial_extensions:
        await bot.load_extension(extension)


@bot.event
async def on_ready():
    """
    Événement déclenché lorsque le bot est prêt et connecté.

    Imprime un message dans la console et charge les extensions définies.
    Démarre également le planificateur pour exécuter la fonction send_joblist deux fois par jour.
    """
    print('Bot is ready.')
    await load_extensions(bot)
    start_scheduler()


# Attributs pour la commande d'aide personnalisée
attributes = {
    'name': "help",
    'aliases': ["helpme"],
    'cooldown': commands.CooldownMapping.from_cooldown(3, 5, commands.BucketType.user),
}

# Définition de la commande d'aide personnalisée
bot.help_command = SupremeHelpCommand(command_attrs=attributes)

# Démarrage du bot avec le token Discord
bot.run(discord_token)

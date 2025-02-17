import discord
import re
import locale
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from utils.utils_internship import send_jobslist
from utils.utils_fulltime import send_cdilist
from utils.progress_fetcher import fetch_progress
from utils.config_loader import config

scheduler = AsyncIOScheduler()

# Définir la locale en français pour formater les mois en français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


async def joblist_morning(bot):
    await send_jobslist(bot)  # Appelez la méthode send_joblist
    print("Updated list internship auto 1!")


async def joblist_evening(bot):
    await send_jobslist(bot)  # Appelez la méthode send_joblist
    print("Updated list internship auto 2!")


async def cdi_morning(bot):
    await send_cdilist(bot)  # Appelez la méthode send_joblist
    print("Updated list full-time auto 1!")


async def cdi_evening(bot):
    await send_cdilist(bot)  # Appelez la méthode send_joblist
    print("Updated list full-time auto 2!")


async def fetch_and_send_progress(bot):
    """Récupère la progression et envoie les embeds dans les salons appropriés."""
    progress_data = await fetch_progress()
    ## print(progress_data)

    if progress_data:
        for item in progress_data:
            progress_emoji = "🟩" * (item['progress'] // 10) + "🟥" * (10 - (item['progress'] // 10))

            # Création de l'embed
            embed = discord.Embed(
                title=f"🛠 {item.get('currentProject', 'Non spécifié')}",
                color=discord.Color.blue() if item['success'] else discord.Color.red()
            )
            embed.add_field(
                name="📊 **Progression**",
                value=f"{item['progress']}% {progress_emoji}",
                inline=False
            )
            # Extraction de la date à partir de 'agenda'
            agenda_str = item.get('agenda', ['Non spécifié'])[0]
            # Expression régulière pour les deux formats possibles
            match = re.search(r"(Fin de la promo:|Fin du projet actuel :)\s*(\d{4}-\d{2}-\d{2})", agenda_str)

            if match:
                date_str = match.group(2)  # Récupère la date extraite (YYYY-MM-DD)
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # Parse la date au format 'YYYY-MM-DD'
                    formatted_date = f"Le {date_obj.day} {date_obj.strftime('%B')} {date_obj.year}"  # Formatée en "Le 7 Juin 2024"
                except ValueError:
                    formatted_date = 'Non spécifié'  # Si la date est mal formée
            else:
                formatted_date = 'Non spécifié'  # Si la date n'a pas été trouvée dans la chaîne

            embed.add_field(
                name="📅 **Échéance**",
                value=formatted_date,
                inline=False
            )
            if 'notes' in item and item['notes']:
                embed.add_field(
                    name="📝 **Notes supplémentaires**",
                    value=item['notes'],
                    inline=False
                )
            embed.set_footer(text=f"Zone01 Normandie - Suivi de progression - {item['promotionName']} ",
                             icon_url="https://example.com/footer-icon.png")

            # Associer chaque promotion à un salon spécifique
            channel_name = f"channel_progress_{item['promotionName'].replace(' ', '_')}"
            channel_id = config.get(channel_name)

            channel_modo_id = 1257310056546963479  # Remplace par l'ID de ton channel
            channel_modo = bot.get_channel(channel_modo_id)

            if channel_id:
                channel = bot.get_channel(channel_id)
                if channel:
                    # Supprimer les anciens messages (sauf le dernier)
                    async for message in channel.history(limit=100):
                        if message.author == bot.user:
                            await message.delete()
                    # Envoi de l'embed dans le salon de la promotion
                    await channel.send(embed=embed)
                else:
                    print(f"Salon avec l'ID {channel_id} pour la promotion {item['promotionName']} non trouvé.")
                    # Création d'un embed d'erreur
                    embed_error = discord.Embed(
                        title="🚫 Erreur Automatique",
                        description=f"Salon avec l'ID {channel_id} pour la promotion {item['promotionName']} non trouvé.",
                        color=discord.Color.red()
                    )
                    await channel_modo.send(embed=embed_error)
            else:
                print(f"Channel non configuré pour la promotion {item['promotionName']}.")
                # Création d'un embed d'erreur
                embed_error = discord.Embed(
                    title="🚫 Erreur Automatique",
                    description=f"Channel non configuré pour la promotion {item['promotionName']}.",
                    color=discord.Color.red()
                )
                await channel_modo.send(embed=embed_error)

    else:
        print("Impossible de récupérer les données de progression pour le moment.")



def start_scheduler(bot):
    # Print the time of the scheduler start
    print(f"Scheduler started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Scheduler jobs with bot parameter
    @scheduler.scheduled_job("cron", hour=9, minute=0)  # Run at 9 AM
    async def schedule_joblist_morning():
        await joblist_morning(bot)
        await cdi_morning(bot)

    @scheduler.scheduled_job("cron", hour=18, minute=0)  # Run at 6 PM
    async def schedule_joblist_evening():
        await joblist_evening(bot)
        await cdi_evening(bot)

    @scheduler.scheduled_job("cron", hour=9, minute=0)  # Run at 9 AM
    async def schedule_fetch_progress_morning():
        await fetch_and_send_progress(bot)

    @scheduler.scheduled_job("cron", hour=18, minute=0)  # Run at 6 PM
    async def schedule_fetch_progress_evening():
        await fetch_and_send_progress(bot)

    scheduler.start()

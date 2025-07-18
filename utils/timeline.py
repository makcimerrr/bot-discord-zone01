import discord
import re
from datetime import datetime
from utils.progress_fetcher import fetch_progress
from utils.config_loader import config

async def fetch_and_send_progress(bot):
    """Récupère la progression et envoie les embeds dans les salons appropriés."""
    progress_data = await fetch_progress()
    ## print(progress_data)

    if progress_data:
        for item in progress_data:
            progress_emoji = "🟩" * (item['progress'] // 10) + "🟥" * (10 - (item['progress'] // 10))

            # Création de l'embed
            embed = discord.Embed(
                title=f"📚 Projet en cours : `{item.get('currentProject', 'Non spécifié')}`",
                description=f"👤 **Promotion** : `{item['promotionName']}`",
                color=discord.Color.green() if item['success'] else discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.set_author(name="Suivi de progression Zone01", icon_url="https://example.com/logo.png")
            embed.add_field(
                name="📈 Progression",
                value=f"`{item['progress']}%`  \n{progress_emoji}",
                inline=True
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
                name="⏳ Échéance estimée",
                value=f"`{formatted_date}`",
                inline=True
            )
            if 'notes' in item and item['notes']:
                embed.add_field(
                    name="📝 **Notes supplémentaires**",
                    value=item['notes'],
                    inline=False
                )
            embed.set_footer(text="Zone01 Normandie • Mise à jour automatique", icon_url="https://example.com/footer-icon.png")

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
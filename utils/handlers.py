from discord import DMChannel
from utils.models import add_response_to_notion

async def handle_dm(bot, message):
    if isinstance(message.channel, DMChannel) and not message.author.bot:
        try:
            user = message.author.name
            response = message.content

            add_response_to_notion(user, response)

            await message.channel.send("✅ Réponse enregistrée, merci !")
            print(f"Réponse enregistrée de {user}")

        except Exception as e:
            print(f"❌ Erreur pour {message.author.name} : {e}")
            await message.channel.send("❌ Une erreur est survenue lors de l'enregistrement.")
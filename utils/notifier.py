import discord
from dotenv import load_dotenv
from utils.config_loader import role_alternants, channel_id_feedback_alternance

load_dotenv(override=True)


async def send_monthly_message(bot):
    try:
        channel = bot.get_channel(channel_id_feedback_alternance)
        if channel is None:
            print(f"❌ Channel ID {channel_id_feedback_alternance} introuvable")
            return

        guild = channel.guild
        role = guild.get_role(role_alternants)
        if not role:
            print(f"❌ Rôle ID {role_alternants} introuvable")
            return

        members = [
            m for m in guild.members if role in m.roles and not m.bot
        ]

        print(f"📬 Envoi à {len(members)} membres")

        for member in members:
            try:
                dm = await member.create_dm()
                await dm.send(
                    "Bonjour ! 👋🏼\n\n"
                    "Merci de répondre à ce message pour nous informer de votre avancée mensuelle dans la formation : projets, audits, alternance, problèmes, etc. 📈\n\n"
                    "💼 Si vous n’avez rien de particulier à signaler, répondez simplement : **R.A.S**.\n\n"
                    "Merci de le faire en un seul message. Seule la dernière réponse sera prise en compte. 🙏🏻\n\n"
                    "Infos utiles : [Clique ici](https://discord.com/channels/905002122309951538/1115929577890533486/1332297087945277461)"
                )
                print(f"✅ DM envoyé à {member.name}")
            except discord.Forbidden:
                print(f"❌ DMs fermés pour {member.name}")
            except Exception as e:
                print(f"❌ Erreur DM {member.name} : {e}")

    except Exception as e:
        print(f"❌ Erreur globale lors de l’envoi : {e}")

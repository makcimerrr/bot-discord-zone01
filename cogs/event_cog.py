import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Modal, TextInput, Button, View
from datetime import datetime, timedelta

# Dictionnaire pour stocker les utilisateurs présents pour chaque événement
event_attendees = {}


class MyView(discord.ui.View):

    @discord.ui.button(label="S'inscrire", style=discord.ButtonStyle.success, emoji="✅")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            event_id = interaction.message.embeds[0].footer.text.split()[-1]

            if event_id not in event_attendees:
                await interaction.response.send_message("Erreur: événement introuvable.", ephemeral=True)
                return

            if interaction.user.id not in event_attendees[event_id]['users']:
                start_time = event_attendees[event_id]['start_time']
                duration = event_attendees[event_id]['duration']
                num_users = len(event_attendees[event_id]['users'])

                user_start_time = start_time + timedelta(minutes=num_users * duration)
                user_end_time = user_start_time + timedelta(minutes=duration)

                event_attendees[event_id]['users'][interaction.user.id] = f"{user_start_time.strftime('%H:%M')} - {user_end_time.strftime('%H:%M')}"

                embed = interaction.message.embeds[0]
                user_list = [f"<@{user_id}> ({time})" for user_id, time in event_attendees[event_id]['users'].items()]
                embed.set_field_at(1, name=f"Présent ({len(event_attendees[event_id]['users'])})", value="\n".join(user_list), inline=True)

                await interaction.message.edit(embed=embed, view=self)
                await interaction.response.send_message("Inscription réussie!", ephemeral=True)
            else:
                await interaction.response.send_message("Vous êtes déjà inscrit à cet événement.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite: {e}", ephemeral=True)

    @discord.ui.button(label="Effacer un étudiant", style=discord.ButtonStyle.primary, emoji="🗑️")
    async def delete_user_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Vous n'avez pas la permission de faire cela.", ephemeral=True)
            return

        try:
            event_id = interaction.message.embeds[0].footer.text.split()[-1]

            if event_id not in event_attendees:
                await interaction.response.send_message("Erreur: événement introuvable.", ephemeral=True)
                return

            if event_attendees[event_id]['users']:
                # Remove the first user in the list
                removed_user_id = next(iter(event_attendees[event_id]['users']))
                del event_attendees[event_id]['users'][removed_user_id]

                embed = interaction.message.embeds[0]
                user_list = [f"<@{user_id}> ({time})" for user_id, time in event_attendees[event_id]['users'].items()]
                embed.set_field_at(1, name=f"Présent ({len(event_attendees[event_id]['users'])})", value="\n".join(user_list), inline=True)

                await interaction.message.edit(embed=embed, view=self)
                await interaction.response.send_message(f"<@{removed_user_id}> a été supprimé de la liste.", ephemeral=True)

                # Check if there's another user to ping
                if event_attendees[event_id]['users']:
                    next_user_id = next(iter(event_attendees[event_id]['users']))
                    await interaction.channel.send(f"<@{next_user_id}>, disponible pour ton entretien ?")
            else:
                await interaction.response.send_message("La liste des utilisateurs est vide.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite: {e}", ephemeral=True)

    @discord.ui.button(label="Supprimer l'embed", style=discord.ButtonStyle.danger, emoji="🚫")
    async def delete_embed_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Vous n'avez pas la permission de faire cela.", ephemeral=True)
            return

        try:
            event_id = interaction.message.embeds[0].footer.text.split()[-1]

            if event_id not in event_attendees:
                await interaction.response.send_message("Erreur: événement introuvable.", ephemeral=True)
                return

            await interaction.message.delete()
            del event_attendees[event_id]

            await interaction.response.send_message("L'événement a été supprimé.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite: {e}", ephemeral=True)

    @discord.ui.button(label="Clôturer les inscriptions", style=discord.ButtonStyle.secondary, emoji="🔒")
    async def close_registrations_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Vous n'avez pas la permission de faire cela.", ephemeral=True)
            return

        try:
            event_id = interaction.message.embeds[0].footer.text.split()[-1]

            if event_id not in event_attendees:
                await interaction.response.send_message("Erreur: événement introuvable.", ephemeral=True)
                return

            # Disable the sign-up button
            self.children[0].disabled = True

            # Update the embed to indicate that registrations are closed
            embed = interaction.message.embeds[0]
            embed.set_footer(text=f"Inscriptions clôturées pour l'événement {event_id}")

            await interaction.message.edit(embed=embed, view=self)
            await interaction.response.send_message("Les inscriptions sont maintenant clôturées.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite: {e}", ephemeral=True)


class EventModal(Modal):
    def __init__(self):
        super().__init__(title="Create Event")

        self.add_item(TextInput(label="Event Title", placeholder="Enter the event title"))
        self.add_item(
            TextInput(label="Description", style=discord.TextStyle.long, placeholder="Enter the event description"))
        self.add_item(TextInput(label="Event Date", placeholder="Enter the event date (JJ/MM/AAAA)"))
        self.add_item(TextInput(label="Event Time", placeholder="Enter the event time (HH:MM - HH:MM)"))
        self.add_item(TextInput(label="Event Duration", placeholder="Enter the duration of one session in minutes"))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Récupère les valeurs de l'input
            title = self.children[0].value
            description = self.children[1].value
            date = self.children[2].value
            time_range = self.children[3].value
            duration = int(self.children[4].value)

            # Parse la plage horaire
            start_time_str, end_time_str = time_range.split(' - ')
            start_time = datetime.strptime(start_time_str, '%H:%M')
            end_time = datetime.strptime(end_time_str, '%H:%M')

            embed = discord.Embed(
                title=title,
                description=description,
                color=discord.Color.blue()
            )
            embed.set_author(name=interaction.user.display_name)
            embed.add_field(name="Event Info:", value=f"📅 {date}\n🕗 {time_range}", inline=False)
            embed.add_field(name="Présent (0)", value="", inline=True)
            event_id = f"{title}-{interaction.user.id}"
            embed.set_footer(text=f"Event ID: {event_id}")

            view = MyView()

            event_attendees[event_id] = {
                'embed': embed,
                'view': view,
                'users': {},
                'start_time': start_time,
                'end_time': end_time,
                'duration': duration
            }

            await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite: {e}", ephemeral=True)


def is_admin():
    async def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.guild_permissions.administrator

    return app_commands.check(predicate)


class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("EventCog is ready.")

    @app_commands.command(name="create_event", description="Creates an event with the provided details.")
    @is_admin()
    async def create_event(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_modal(EventModal())
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite: {e}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(EventCog(bot))

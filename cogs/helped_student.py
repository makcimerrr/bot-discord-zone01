import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Modal, TextInput, Button, View
from utils.config_loader import role_help, role_p1_2023, role_p2_2023, role_p1_2024, channel_inter_promo

# Dictionnaire pour les IDs de canal associés aux rôles
role_channel_mapping = {
    role_p1_2023: 1045019188927938641,  # Remplacez par les IDs de vos canaux
    role_p2_2023: 1133380731461193769,
    role_p1_2024: 1222587487969611906
}

# Création de la classe pour les boutons
class HelpView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot  # Ajout du bot comme attribut
        self.session_open = True  # État initial de la session

    @discord.ui.button(label="Fermer la session", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Vérifiez si l'utilisateur a les permissions nécessaires
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Vous n'avez pas la permission de faire cela.", ephemeral=True)
            return

        # Toggle entre fermer et réouvrir la session
        if self.session_open:
            button.label = "Réouvrir la session"
            button.style = discord.ButtonStyle.success
            button.emoji = "🔓"
            self.session_open = True
            await interaction.response.send_message("La session a été fermée.", ephemeral=True)
        else:
            button.label = "Fermer la session"
            button.style = discord.ButtonStyle.danger
            button.emoji = "🔒"
            self.session_open = False
            await interaction.response.send_message("La session a été réouverte.", ephemeral=True)

        # Mettre à jour le message avec la vue modifiée
        await interaction.message.edit(view=self)

    @discord.ui.button(label="Demander de l'aide", style=discord.ButtonStyle.success, emoji="✅")
    async def ask_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.session_open:
            # Si la session est fermée, désactiver l'interaction
            await interaction.response.send_message("La session est actuellement fermée.", ephemeral=True)
            return

        role = interaction.guild.get_role(role_help)
        if role:
            # Vérifie si l'utilisateur a déjà le rôle
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)  # Enlève le rôle
                # Ne modifie le pseudo que si le préfixe 🚨 est présent
                if interaction.user.nick and interaction.user.nick.startswith("🚨"):
                    # Supprime le préfixe 🚨 sans toucher au reste du pseudo
                    original_nick = interaction.user.nick.replace("🚨 ", "", 1)
                    await interaction.user.edit(nick=original_nick)

                # Change le bouton pour revenir à l'état initial
                # button.label = "Demander de l'aide"
                # button.style = discord.ButtonStyle.success
                # button.emoji = "✅"

                # await interaction.message.edit(view=self)
                await interaction.response.send_message("Le rôle vous a été retiré et votre pseudo a été réinitialisé.",
                                                        ephemeral=True)
                # Supprimer les messages d'aide existants dans le canal du rôle
                # user_roles = [role.id for role in interaction.user.roles]
                # channel_id = None
                channel_id = channel_inter_promo

                # Vérifier les rôles et sélectionner le canal approprié
                # for role_id, target_channel_id in role_channel_mapping.items():
                    # if role_id in user_roles:
                        # channel_id = target_channel_id
                        # break

                if channel_id:
                    channel = interaction.guild.get_channel(channel_id)
                    if channel:
                        # Recherche des messages dans le canal correspondant
                        async for message in channel.history(limit=100):
                            if message.author == self.bot.user and "a besoin d'aide" in message.content and interaction.user.mention in message.content:
                                try:
                                    await message.delete()
                                    #print(f"Deleted message: {message.id}")  # Debugging
                                except discord.Forbidden:
                                    print("Bot lacks permission to delete messages.")  # Debugging
                                except discord.HTTPException as e:
                                    print(f"Failed to delete message: {e}")  # Debugging
                    else:
                        await interaction.followup.send("Le canal pour envoyer le message d'aide est introuvable.", ephemeral=True)
                else:
                    await interaction.followup.send("Aucun canal correspondant aux rôles de l'utilisateur n'a été trouvé.", ephemeral=True)

            else:
                await interaction.user.add_roles(role)  # Ajoute le rôle
                # Ajoute le préfixe 🚨 uniquement si le pseudo actuel n'a pas déjà ce préfixe
                if interaction.user.nick is None or not interaction.user.nick.startswith("🚨"):
                    new_nickname = f"🚨 {interaction.user.nick or interaction.user.name}"
                    await interaction.user.edit(nick=new_nickname)

                # Change l'aspect du bouton une fois le rôle attribué
                # button.label = "Rôle attribué"
                # button.style = discord.ButtonStyle.danger  # Change la couleur du bouton
                # button.emoji = "❌"

                # await interaction.message.edit(view=self)
                await interaction.response.send_message("Vous avez été attribué le rôle et votre pseudo a été modifié.",
                                                        ephemeral=True)

                # Determine the appropriate channel based on the user's roles
                # channel_id = None
                channel_id = channel_inter_promo
                # user_roles = [role.id for role in interaction.user.roles]  # Get the list of role IDs of the user

                #print("User Roles:", user_roles)  # Debugging line
                #print("Role Channel Mapping:", role_channel_mapping)  # Debugging line

                # for role_id, target_channel_id in role_channel_mapping.items():
                    # if role_id in user_roles:
                        # channel_id = target_channel_id
                        # break

                if channel_id:
                    channel = interaction.guild.get_channel(channel_id)
                    if channel:
                        await channel.send(f"{interaction.user.mention} a besoin d'aide !")
                    else:
                        await interaction.followup.send(
                            "Le canal pour envoyer le message d'aide est introuvable.", ephemeral=True)
                else:
                    await interaction.followup.send(
                        "Aucun canal correspondant aux rôles de l'utilisateur n'a été trouvé.", ephemeral=True)
        else:
            await interaction.followup.send("Le rôle pour la demande d'aide n'existe pas.", ephemeral=True)

def is_admin():
    async def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.guild_permissions.administrator

    return app_commands.check(predicate)

# Création de la commande slash
class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("EventCog is ready.")

    @app_commands.command(name="send_help_embed", description="Envoie un embed d'aide dans le canal spécifié.")
    @is_admin()
    async def send_help_embed(self, interaction: discord.Interaction, channel: discord.TextChannel):
        embed_description = (
            "Pour demander de l'aide auprès d'autres apprenants de ta promo, clique sur le bouton ci-dessous\n\n> Une fois ta demande effectuée, tu te verras attribuer un rôle et un pseudo. Des apprenants viendront sous peu t'apporter de l'aide !"
        )

        embed = discord.Embed(title="Besoin d'aide ?", description=embed_description, colour=0x002e7a,
                              timestamp=discord.utils.utcnow())
        embed.set_author(name="Info")
        embed.set_footer(text="Zone01",
                         icon_url="https://zone01rouennormandie.org/wp-content/uploads/2024/03/01talent-profil-400x400-1.jpg")

        view = HelpView(self.bot)

        # Envoyer l'embed dans le canal spécifié
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"L'embed d'aide a été envoyé dans {channel.mention}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Modal, TextInput, Button, View
from utils.config_loader import role_help

# Création de la classe pour les boutons
class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
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
                button.label = "Demander de l'aide"
                button.style = discord.ButtonStyle.success
                button.emoji = "✅"

                await interaction.message.edit(view=self)
                await interaction.response.send_message("Le rôle vous a été retiré et votre pseudo a été réinitialisé.",
                                                        ephemeral=True)
            else:
                await interaction.user.add_roles(role)  # Ajoute le rôle
                # Ajoute le préfixe 🚨 uniquement si le pseudo actuel n'a pas déjà ce préfixe
                if interaction.user.nick is None or not interaction.user.nick.startswith("🚨"):
                    new_nickname = f"🚨 {interaction.user.nick or interaction.user.name}"
                    await interaction.user.edit(nick=new_nickname)

                # Change l'aspect du bouton une fois le rôle attribué
                button.label = "Rôle attribué"
                button.style = discord.ButtonStyle.danger  # Change la couleur du bouton
                button.emoji = "❌"

                await interaction.message.edit(view=self)
                await interaction.response.send_message("Vous avez été attribué le rôle et votre pseudo a été modifié.",
                                                        ephemeral=True)
        else:
            await interaction.response.send_message("Le rôle pour la demande d'aide n'existe pas.", ephemeral=True)

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

        view = HelpView()

        # Envoyer l'embed dans le canal spécifié
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"L'embed d'aide a été envoyé dans {channel.mention}.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(HelpCommand(bot))

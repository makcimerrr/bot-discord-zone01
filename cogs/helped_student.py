import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from utils.config_loader import role_helped


# Création de la classe pour les boutons
class HelpView(View):

    @discord.ui.button(label="Fermer la session", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close_session(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Vous n'avez pas la permission de faire cela.", ephemeral=True)
            return

        self.children[1].disabled = True  # Désactiver le bouton pour les utilisateurs
        await interaction.message.edit(view=self)  # Mettre à jour le message avec la vue modifiée
        await interaction.response.send_message("La session a été fermée.", ephemeral=True)

    @discord.ui.button(label="Demander de l'aide", style=discord.ButtonStyle.success, emoji="✅")
    async def request_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Attribution du rôle et modification du pseudo ici
        role = interaction.guild.get_role(role_helped)
        if role:
            await interaction.user.add_roles(role)
            new_nickname = f"🚨 {interaction.user.name}"
            await interaction.user.edit(nick=new_nickname)
            await interaction.response.send_message("Vous avez été attribué le rôle et votre pseudo a été modifié.",
                                                    ephemeral=True)
        else:
            await interaction.response.send_message("Le rôle pour la demande d'aide n'existe pas.", ephemeral=True)


# Création de la commande slash
class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="send_help_embed", description="Envoie un embed d'aide dans le canal spécifié.")
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

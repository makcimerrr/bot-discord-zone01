import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Modal, TextInput, View


class EmbedModal(Modal):
    def __init__(self, channel: discord.TextChannel):
        super().__init__(title="Créer un Embed")
        self.channel = channel

        # Champs pour le formulaire
        self.add_item(TextInput(label="Titre de l'embed", placeholder="Entrez le titre de l'embed"))
        self.add_item(TextInput(label="Description de l'embed", style=discord.TextStyle.long, placeholder="Entrez la description de l'embed"))
        self.add_item(TextInput(label="Détails",style=discord.TextStyle.long, placeholder="Entrez les détails de l'embed"))
        self.add_item(TextInput(label="Nombre de sessions",style=discord.TextStyle.short, placeholder="Entrez le nombre de sessions"))
        self.add_item(TextInput(label="Nombre max de réactions par session",style=discord.TextStyle.short, placeholder="Entrez le nombre max de réactions par session"))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Récupère les valeurs des champs
            title = self.children[0].value
            description = self.children[1].value
            details = self.children[2].value
            num_responses = int(self.children[3].value)
            max_reactions = int(self.children[4].value)

            # Crée l'embed avec les informations fournies
            embed = discord.Embed(title=title, description=description, color=discord.Color.green())
            embed.set_author(name="🚨 - " + interaction.user.display_name)
            embed.add_field(name="📜 - Détails:", value=details, inline=False)
            embed.timestamp = discord.utils.utcnow()

            await self.channel.send(f"@everyone", allowed_mentions=discord.AllowedMentions(everyone=True))

            # Envoie l'embed dans le canal spécifié
            message = await self.channel.send(embed=embed)

            # Ajoute les réactions sous l'embed
            emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']  # Liste d'émojis possibles
            for i in range(min(num_responses, len(emojis))):
                await message.add_reaction(emojis[i])

            await interaction.response.send_message(
                f"Embed envoyé dans {self.channel.mention} avec {num_responses} sessions et max {max_reactions} réactions par session.",
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(f"Erreur lors de la création de l'embed : {str(e)}", ephemeral=True)


def is_admin():
    async def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.guild_permissions.administrator

    return app_commands.check(predicate)


class EmbedCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("EmbedCog is ready.")

    @app_commands.command(name="create_embed", description="Crée un embed avec les détails fournis et l'envoie dans un canal spécifié.")
    @is_admin()
    async def create_embed(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            modal = EmbedModal(channel)
            await interaction.response.send_modal(modal)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite : {str(e)}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(EmbedCog(bot))

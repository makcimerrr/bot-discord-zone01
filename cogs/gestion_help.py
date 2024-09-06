import discord
from discord.ext import commands


async def send_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="🚫 Commande Inconnue",
            description="La commande que vous avez essayée n'existe pas. Veuillez vérifier la commande et réessayer.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Utilisez !help pour voir les commandes disponibles.")
    else:
        embed = discord.Embed(
            title="❌ Erreur",
            description=str(error),
            color=discord.Color.red()
        )
        embed.set_footer(text="Veuillez vérifier la commande et réessayer.")

    await ctx.send(embed=embed)


class SupremeHelpCommand(commands.Cog, commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="🔧 Commandes du Bot",
            description="Voici toutes les commandes disponibles pour ce bot.",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url="https://i.imgur.com/vn0HoFx.png")  # Ajouter une image d'illustration

        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                cog_name = getattr(cog, "qualified_name", "Aucune Catégorie")
                command_list = "\n".join(f"`{self.get_command_signature(c)}`" for c in filtered)
                embed.add_field(name=f"📁 {cog_name}", value=command_list, inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=self.get_command_signature(command),
            description=command.help or "Aucune description disponible.",
            color=discord.Color.blurple()
        )
        if alias := command.aliases:
            embed.add_field(name="🔄 Alias", value=", ".join(alias), inline=False)
        if command.cog:
            embed.add_field(name="📁 Catégorie", value=command.cog.qualified_name, inline=False)

        embed.set_footer(text="Pour plus d'informations sur d'autres commandes, utilisez !help")
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_help_embed(self, title, description, commands):
        embed = discord.Embed(
            title=title,
            description=description or "Aide non trouvée.",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url="https://i.imgur.com/vn0HoFx.png")  # Ajouter une image d'illustration

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.help or "Aucune description disponible.",
                    inline=False
                )

        embed.set_footer(text="Pour plus d'informations, utilisez !help")
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        title = cog.qualified_name or "Aucune Catégorie"
        await self.send_help_embed(f'📚 {title} Category', cog.description, cog.get_commands())


async def setup(bot):
    await bot.add_cog(SupremeHelpCommand(bot))
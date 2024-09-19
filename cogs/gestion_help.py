import asyncio
from datetime import datetime

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


# Fonction globale pour vérifier la réaction "✅" sur un message spécifique
def check(reaction, user, message, bot):
    return (
            user != bot.user  # Ne pas prendre en compte les réactions du bot lui-même
            and str(reaction.emoji) == "✅"  # Vérifie si la réaction est "✅"
            and reaction.message.id == message.id  # Vérifie si la réaction est sur le bon message
    )


class SupremeHelpCommand(commands.Cog, commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        # Supprimer le message de l'utilisateur
        await self.context.message.delete()

        # Définition des icônes pour chaque cog
        cog_icons = {
            "Administration": "🛠️",
            "Configuration": "⚙️",
            "Utilitaire": "🧰",
            "Aucune Catégorie": "❓",
        }

        embed = discord.Embed(
            title="🔧 Commandes du Bot",
            description="Pour avoir la description et l'utilisation d'une commande faites :\n" +
                        "!help <nom de la commande>\n" +
                        "_Les < > ne sont pas à inclure dans la commande_",
            color=discord.Color.blurple()
        )

        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                # Obtenir le nom du cog et son icône associée
                cog_name = getattr(cog, "qualified_name", "Aucune Catégorie")
                cog_icon = cog_icons.get(cog_name, "❓")  # Icône par défaut si aucune correspondance
                command_count = len(filtered)  # Nombre de commandes disponibles dans ce cog

                # Liste des commandes sans préfixe, alignées horizontalement
                command_list = " • ".join(f"`{c.name}`" for c in filtered)

                # Ajouter un champ avec l'icône et le nom du cog
                embed.add_field(
                    name=f"{cog_icon} {cog_name} - {command_count}",
                    value=command_list,
                    inline=False
                )

        # Récupérer l'icône du bot et l'heure actuelle formatée
        bot_icon = self.context.bot.user.avatar.url if self.context.bot.user.avatar else None
        current_time = datetime.now().strftime("Aujourd’hui à %H:%M")

        # Ajouter le footer personnalisé
        embed.set_footer(text=f"Tous Droits Réservés • {current_time}", icon_url=bot_icon)

        channel = self.get_destination()
        message = await channel.send(embed=embed)

        # Ajoute une réaction "✅" à l'embed
        await message.add_reaction("✅")

        try:
            # Attend qu'une réaction soit ajoutée qui correspond aux critères du `check`
            reaction, user = await self.context.bot.wait_for(
                "reaction_add", timeout=60.0, check=lambda r, u: check(r, u, message, self.context.bot)
            )
            await message.delete()  # Supprime le message embed si la réaction est ajoutée
        except asyncio.TimeoutError:
            await message.clear_reactions()  # Supprime les réactions si le délai expire

    async def send_command_help(self, command):
        # Vérifier si la commande existe
        if command not in self.context.bot.commands:
            await self.context.message.delete()
            embed = discord.Embed(
                title="🚫 Commande Introuvable",
                description=f"Aucune commande appelée `{command.name}` trouvée. Veuillez vérifier le nom de la commande et réessayer.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Utilisez !help pour voir les commandes disponibles.")
            await self.get_destination().send(embed=embed)
            return

        await self.context.message.delete()

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
        message = await channel.send(embed=embed)
        # Ajoute une réaction "✅" à l'embed
        await message.add_reaction("✅")

        try:
            # Attend qu'une réaction soit ajoutée qui correspond aux critères du `check`
            reaction, user = await self.context.bot.wait_for(
                "reaction_add", timeout=60.0, check=lambda r, u: check(r, u, message, self.context.bot)
            )
            await message.delete()  # Supprime le message embed si la réaction est ajoutée
        except asyncio.TimeoutError:
            await message.clear_reactions()  # Supprime les réactions si le délai expire

    async def send_help_embed(self, title, description, commands):
        await self.context.message.delete()

        embed = discord.Embed(
            title=title,
            description=description or "Aide non trouvée.",
            color=discord.Color.blurple()
        )

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.help or "Aucune description disponible.",
                    inline=False
                )

        embed.set_footer(text="Pour plus d'informations, utilisez !help")
        channel = self.get_destination()
        message = await channel.send(embed=embed)

        # Ajoute une réaction "✅" à l'embed
        await message.add_reaction("✅")

        try:
            # Attend qu'une réaction soit ajoutée qui correspond aux critères du `check`
            reaction, user = await self.context.bot.wait_for(
                "reaction_add", timeout=60.0, check=lambda r, u: check(r, u, message, self.context.bot)
            )
            await message.delete()  # Supprime le message embed si la réaction est ajoutée
        except asyncio.TimeoutError:
            await message.clear_reactions()  # Supprime les réactions si le délai expire

    async def send_group_help(self, group):
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        title = cog.qualified_name or "Aucune Catégorie"
        await self.send_help_embed(f'📚 {title} Category', cog.description, cog.get_commands())

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await send_command_error(ctx, error)


async def setup(bot):
    await bot.add_cog(SupremeHelpCommand(bot))

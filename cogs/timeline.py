import discord
import json
from discord.ext import commands
from datetime import datetime, timedelta
from utils.config_loader import promotions, projects, holidays


class TimelineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.promotions = promotions
        self.projects = projects
        self.holidays = holidays
        self.promo_roles = {
            "🧭|Fondateur": "P1_2023",
            "🙏| Membre": "P2_2023",
        }
        # Dictionnaire des synonymes de promotions
        self.promotion_synonyms = {
            "P1_2023": ["p1", "P1", "promotion1", "première_promotion", "p12023", "p1_2023", "2023p1", "2023_p1"],
            "P2_2023": ["p2", "P2", "promotion2", "deuxième_promotion", "p22023", "p2_2023", "2023p2", "2023_p2"],
        }

    def calculate_percentage(self, start_date, end_date, current_date):
        total_days = (end_date - start_date).days
        elapsed_days = (current_date - start_date).days
        if total_days <= 0:
            return 0
        return min((elapsed_days / total_days) * 100, 100)

    def get_current_project(self, promotion, current_date):
        def get_weekdays(start_date, end_date):
            weekdays = []
            current_date = start_date
            while current_date <= end_date:
                if current_date.weekday() < 5:  # 0 = Monday, 4 = Friday
                    weekdays.append(current_date)
                current_date += timedelta(days=1)
            return weekdays

        def get_holidays(start_date, end_date, holidays):
            holidays_dates = []
            for holiday_periods in holidays.values():
                for period in holiday_periods:
                    holiday_start = datetime.strptime(period["start"], "%Y-%m-%d")
                    holiday_end = datetime.strptime(period["end"], "%Y-%m-%d")
                    if holiday_end >= start_date and holiday_start <= end_date:
                        holidays_dates.extend(get_weekdays(max(start_date, holiday_start), min(end_date, holiday_end)))
            return holidays_dates

        def process_project(name, start_date, project_weeks, holidays, current_date):
            effective_days = []
            end_date = start_date
            while project_weeks > 0:
                next_end_date = end_date + timedelta(weeks=project_weeks)
                project_effective_days, next_end_date = calculate_effective_days(end_date, next_end_date, holidays)
                effective_days.extend(project_effective_days)
                holidays_dates = get_holidays(end_date, next_end_date, holidays)
                if holidays_dates:
                    first_holiday = min(holidays_dates)
                    holiday_end = max(holidays_dates)  # Correctly define holiday_end
                    end_date = holiday_end + timedelta(days=1)
                    project_weeks -= (next_end_date - end_date).days // 7
                else:
                    end_date = next_end_date
                    project_weeks = 0
            if start_date <= current_date <= end_date:
                progress = self.calculate_percentage(start_date, end_date, current_date)
                return name, start_date, end_date, progress
            return None, end_date, None, 0

        def calculate_effective_days(start_date, end_date, holidays):
            weekdays = get_weekdays(start_date, end_date)
            holidays_dates = get_holidays(start_date, end_date, holidays)
            effective_days = [day for day in weekdays if day not in holidays_dates]
            return effective_days, end_date

        try:
            current_date = datetime.today()
            start_date = datetime.strptime(promotion["start"], "%Y-%m-%d")

            for project in self.projects["Golang"]:
                project_name, start_date, _, progress = process_project(project["name"], start_date,
                                                                        project["project_time_week"], holidays,
                                                                        current_date)
                if project_name:
                    return project_name, "Golang", progress

            if "piscine-js-start" in promotion and promotion["piscine-js-start"] != "NaN":
                piscine_js_start = datetime.strptime(promotion["piscine-js-start"], "%Y-%m-%d")
                piscine_js_end = datetime.strptime(promotion["piscine-js-end"], "%Y-%m-%d")
                start_date = piscine_js_end + timedelta(days=1)
                for project in self.projects["Javascript"]:
                    project_name, start_date, _, progress = process_project(project["name"], start_date,
                                                                            project["project_time_week"], holidays,
                                                                            current_date)
                    if project_name:
                        return project_name, "Javascript", progress

            if "piscine-rust-start" in promotion and promotion["piscine-rust-start"] != "NaN":
                piscine_rust_start = datetime.strptime(promotion["piscine-rust-start"], "%Y-%m-%d")
                piscine_rust_end = datetime.strptime(promotion["piscine-rust-end"], "%Y-%m-%d")
                start_date = piscine_rust_end + timedelta(days=1)
                for project in self.projects["Rust"]:
                    project_name, start_date, _, progress = process_project(project["name"], start_date,
                                                                            project["project_time_week"], holidays,
                                                                            current_date)
                    if project_name:
                        return project_name, "Rust", progress

            return "Aucun projet actuel", "Aucune catégorie", 0

        except Exception as e:
            print(f"Erreur: {e}")
            return "Erreur lors du calcul du projet actuel", "Erreur", 0

    # Commande pour afficher le projet actuel d'une promotion en prenant en compte les synonymes
    @commands.command(name='currentproject')
    async def current_project(self, ctx, *, term: str):
        try:
            # Normaliser le terme recherché
            term = term.lower()

            # Trouver la promotion correspondant au terme ou à l'un de ses synonymes
            promotion_name = None
            for promo, details in self.promotions.items():
                # Vérifier le nom de la promotion
                if promo.lower() == term:
                    promotion_name = promo
                    break
                # Vérifier les synonymes de la promotion
                synonyms = details[0].get("synonym", [])
                if term in [syn.lower() for syn in synonyms]:
                    promotion_name = promo
                    break

            # Si aucune promotion n'a été trouvée
            if not promotion_name:
                embed = discord.Embed(
                    title=":x: Promotion non trouvée",
                    description=f"Aucune promotion trouvée pour le terme : `{term}`.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            # Récupérer les données de la promotion
            promotion = self.promotions.get(promotion_name)
            if not promotion:
                embed = discord.Embed(
                    title=":x: Promotion non trouvée",
                    description=f"Aucune promotion trouvée pour le nom : `{promotion_name}`.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            # Calculer le projet actuel, la catégorie et la progression
            current_project, category, progress = self.get_current_project(promotion[0], datetime.today())

            # Créer l'embed de réponse avec les informations de la promotion
            embed = discord.Embed(
                title=f":calendar: Promotion: {promotion_name}",
                color=discord.Color.blue()
            )
            embed.add_field(name=":dart: Projet Actuel", value=f"{current_project} ({category})", inline=True)
            embed.add_field(name=":bar_chart: Progression", value=f"{progress:.2f}%", inline=True)

            # Envoyer l'embed
            await ctx.send(embed=embed)

        except Exception as e:
            # En cas d'erreur, envoyer un message d'erreur sous forme d'embed
            embed = discord.Embed(
                title=":warning: Erreur",
                description=f"Une erreur est survenue : {e}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(name='listpromos')
    async def list_promotions(self, ctx):
        """
        Commande pour afficher toutes les promotions disponibles
        """
        try:
            # Créez un embed pour afficher toutes les promotions
            embed = discord.Embed(
                title=":books: Liste des Promotions Disponibles",
                description="Voici la liste des promotions disponibles avec leurs dates de début et de fin.",
                color=discord.Color.green()
            )

            # Boucle à travers toutes les promotions
            for promo_name, promo_data in self.promotions.items():
                start_date = promo_data[0]["start"]
                end_date = promo_data[0]["end"]
                piscine_js_start = promo_data[0].get("piscine-js-start", "Non spécifiée")
                piscine_rust_start = promo_data[0].get("piscine-rust-start", "Non spécifiée")

                # Format des dates
                start_date_str = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d %b %Y")
                end_date_str = datetime.strptime(end_date, "%Y-%m-%d").strftime("%d %b %Y")

                # Ajouter un champ pour chaque promotion dans l'embed
                embed.add_field(
                    name=f"Promotion {promo_name}",
                    value=(
                        f"**Début :** {start_date_str}\n"
                        f"**Fin :** {end_date_str}\n"
                        f"**Piscine JS :** {piscine_js_start}\n"
                        f"**Piscine Rust :** {piscine_rust_start}"
                    ),
                    inline=False
                )

            # Envoyer l'embed dans le canal
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title=":warning: Erreur",
                description=f"Une erreur est survenue lors de la récupération des promotions : {e}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(name='promoprogress')
    async def promotions_progress(self, ctx):
        """
        Commande pour afficher la progression de toutes les promotions
        """
        try:
            # Créez un embed pour afficher la progression des promotions
            embed = discord.Embed(
                title=":bar_chart: Progression des Promotions",
                description="Voici la progression de toutes les promotions en cours.",
                color=discord.Color.blue()
            )

            current_date = datetime.today()

            # Boucle à travers toutes les promotions pour calculer leur progression
            for promo_name, promo_data in self.promotions.items():
                start_date = datetime.strptime(promo_data[0]["start"], "%Y-%m-%d")
                end_date = datetime.strptime(promo_data[0]["end"], "%Y-%m-%d")

                progress = self.calculate_percentage(start_date, end_date, current_date)

                # Ajouter un champ pour chaque promotion avec sa progression
                embed.add_field(
                    name=f"Promotion {promo_name}",
                    value=f"Progression : **{progress:.2f}%**\nDébut : {start_date.strftime('%d %b %Y')}\nFin : {end_date.strftime('%d %b %Y')}",
                    inline=False
                )

            # Envoyer l'embed dans le canal
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title=":warning: Erreur",
                description=f"Une erreur est survenue lors du calcul de la progression des promotions : {e}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(name='projectsprogress')
    async def projects_progress(self, ctx):
        """
        Commande pour afficher le projet actuel et la progression pour chaque promotion
        """
        try:
            # Créez un embed pour afficher la progression des projets par promotion
            embed = discord.Embed(
                title=":clipboard: Projet actuel par Promotion",
                description="Voici le projet actuel et la progression pour chaque promotion.",
                color=discord.Color.purple()
            )

            current_date = datetime.today()

            # Boucle à travers toutes les promotions
            for promo_name, promo_data in self.promotions.items():
                project_name, category, progress = self.get_current_project(promo_data[0], current_date)

                # Ajouter un champ pour chaque promotion avec son projet et progression
                embed.add_field(
                    name=f"Promotion {promo_name}",
                    value=(
                        f"**Projet actuel :** {project_name}\n"
                        f"**Catégorie :** {category}\n"
                        f"**Progression :** {progress:.2f}%"
                    ),
                    inline=False
                )

            # Envoyer l'embed dans le canal
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title=":warning: Erreur",
                description=f"Une erreur est survenue lors de la récupération des projets : {e}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    def find_oldest_promotion(self, roles):
        """
        Trouve la promotion la plus ancienne en fonction des rôles d'un utilisateur.
        """
        promo_dates = {}  # Stockera les dates de début des promotions
        for role in roles:
            if role.name in self.promo_roles:
                promo_key = self.promo_roles[role.name]
                promo_data = self.promotions.get(promo_key)
                if promo_data:
                    start_date = datetime.strptime(promo_data[0]["start"], "%Y-%m-%d")
                    promo_dates[promo_key] = start_date

        # Trouver la promotion la plus ancienne (avec la date de début la plus ancienne)
        if promo_dates:
            oldest_promo = min(promo_dates, key=promo_dates.get)
            return oldest_promo
        return None

    @commands.command(name='studentproject')
    async def student_project(self, ctx, member: discord.Member = None):
        """
        Affiche le projet actuel d'un étudiant en fonction de son rôle (promotion).
        Si l'étudiant a plusieurs rôles de promotion, la promotion la plus ancienne est choisie.
        """
        member = member or ctx.author  # Si aucun membre n'est mentionné, prend l'auteur du message

        try:
            # Trouver la promotion la plus ancienne en fonction des rôles de l'utilisateur
            promo_name = self.find_oldest_promotion(member.roles)

            if not promo_name:
                embed = discord.Embed(
                    title=":warning: Erreur",
                    description=f"{member.display_name} n'a pas de rôle associé à une promotion.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            # Récupérer la promotion à partir des données
            promotion_data = self.promotions.get(promo_name)
            if not promotion_data:
                await ctx.send(f"Promotion {promo_name} non trouvée dans les données.")
                return

            # Obtenir le projet actuel de l'étudiant
            current_project, category, progress = self.get_current_project(promotion_data[0], datetime.today())

            # Créer un embed pour afficher le projet et la progression
            embed = discord.Embed(
                title=f":mortar_board: Projet actuel pour {member.display_name}",
                description=f"Promotion : {promo_name}",
                color=discord.Color.green()
            )
            embed.add_field(name="Projet Actuel", value=f"{current_project} ({category})", inline=False)
            embed.add_field(name="Progression", value=f"{progress:.2f}%", inline=False)

            # Envoyer l'embed
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title=":warning: Erreur",
                description=f"Une erreur est survenue lors de la récupération du projet : {e}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    # Afficher les vacances
    @commands.command(name='showholidays')
    async def show_holidays(self, ctx):
        """
        Affiche toutes les vacances enregistrées.
        """
        embed = discord.Embed(title="Vacances", color=discord.Color.blue())
        for name, periods in self.holidays.items():
            holidays_str = ""
            for period in periods:
                holidays_str += f"Début: {period['start']}, Fin: {period['end']}\n"
            embed.add_field(name=name, value=holidays_str, inline=False)
        await ctx.send(embed=embed)

    # Afficher les projets
    @commands.command(name='showprojects')
    async def show_projects(self, ctx):
        """
        Affiche tous les projets et leurs durées.
        """
        embed = discord.Embed(title="Projets", color=discord.Color.green())
        for category, projects_list in self.projects.items():
            project_str = ""
            for project in projects_list:
                project_str += f"Nom: {project['name']}, Durée: {project['project_time_week']} semaines\n"
            embed.add_field(name=category, value=project_str, inline=False)
        await ctx.send(embed=embed)

    # Afficher les dates de promotion
    @commands.command(name='showpromotions')
    async def show_promotions(self, ctx):
        """
        Affiche les dates de toutes les promotions.
        """
        embed = discord.Embed(title="Promotions", color=discord.Color.purple())
        for promo_name, promo_data in self.promotions.items():
            promo_str = f"Début: {promo_data[0]['start']}, Fin: {promo_data[0]['end']}\n"
            if promo_data[0]["piscine-js-start"] != "NaN":
                promo_str += f"Piscine JS : {promo_data[0]['piscine-js-start']} - {promo_data[0]['piscine-js-end']}\n"
            if promo_data[0]["piscine-rust-start"] != "NaN":
                promo_str += f"Piscine Rust : {promo_data[0]['piscine-rust-start']} - {promo_data[0]['piscine-rust-end']}\n"
            embed.add_field(name=promo_name, value=promo_str, inline=False)
        await ctx.send(embed=embed)

# Ajouter ou modifier des vacances
    @commands.command(name='addholiday')
    async def add_holiday(self, ctx, holiday_name: str, start_date: str, end_date: str):
        """
        Ajoute ou modifie une période de vacances.
        Format des dates : AAAA-MM-JJ
        """
        try:
            new_holiday = {
                "start": start_date,
                "end": end_date
            }

            if holiday_name in self.holidays:
                self.holidays[holiday_name].append(new_holiday)
            else:
                self.holidays[holiday_name] = [new_holiday]

            # Sauvegarde dans le fichier JSON
            with open("data/holidays.json", "w") as f:
                json.dump(self.holidays, f, indent=4)

            await ctx.send(f"Vacances {holiday_name} ajoutées/modifiées avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout/modification des vacances : {e}")


    # Ajouter ou modifier un projet
    @commands.command(name='addproject')
    async def add_project(self, ctx, category: str, project_name: str, project_time_week: int):
        """
        Ajoute ou modifie un projet dans une catégorie donnée.
        """
        try:
            new_project = {
                "name": project_name,
                "project_time_week": project_time_week
            }

            if category in self.projects:
                self.projects[category].append(new_project)
            else:
                self.projects[category] = [new_project]

            # Sauvegarde dans le fichier JSON
            with open("data/projects.json", "w") as f:
                json.dump(self.projects, f, indent=4)

            await ctx.send(f"Projet {project_name} ajouté/modifié avec succès dans la catégorie {category}.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout/modification du projet : {e}")


    # Ajouter ou modifier une promotion
    @commands.command(name='addpromotion')
    async def add_promotion(self, ctx, promo_name: str, start_date: str, end_date: str, piscine_js_start: str = "NaN", piscine_js_end: str = "NaN", piscine_rust_start: str = "NaN", piscine_rust_end: str = "NaN"):
        """
        Ajoute ou modifie une promotion.
        Format des dates : AAAA-MM-JJ
        """
        try:
            new_promo = [{
                "start": start_date,
                "end": end_date,
                "piscine-js-start": piscine_js_start,
                "piscine-js-end": piscine_js_end,
                "piscine-rust-start": piscine_rust_start,
                "piscine-rust-end": piscine_rust_end
            }]

            self.promotions[promo_name] = new_promo

            # Sauvegarde dans le fichier JSON
            with open("data/promotions.json", "w") as f:
                json.dump(self.promotions, f, indent=4)

            await ctx.send(f"Promotion {promo_name} ajoutée/modifiée avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout/modification de la promotion : {e}")

    @commands.command(name='addsynonym')
    async def add_synonym(self, ctx, promo_name: str, synonym: str):
        """
        Ajoute un synonyme à une promotion existante.
        """
        try:
            # Vérifie si la promotion existe
            if promo_name in self.promotions:
                # Ajoute le synonyme dans le champ 'synonym'
                if "synonym" in self.promotions[promo_name][0]:
                    if synonym not in self.promotions[promo_name][0]["synonym"]:
                        self.promotions[promo_name][0]["synonym"].append(synonym)
                else:
                    self.promotions[promo_name][0]["synonym"] = [synonym]

                # Sauvegarde les modifications dans le fichier JSON
                with open("data/promotions.json", "w") as f:
                    json.dump(self.promotions, f, indent=4)

                await ctx.send(f"Synonyme '{synonym}' ajouté à la promotion '{promo_name}' avec succès.")
            else:
                await ctx.send(f"Promotion '{promo_name}' non trouvée.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout du synonyme : {e}")


# Ajoutez le cog au bot
async def setup(bot):
    await bot.add_cog(TimelineCog(bot))

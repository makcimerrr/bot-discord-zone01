import discord
import asyncio

from utils.utils_function import contains_forbidden_words, extract_technologies
from utils.config_loader import forum_channel_id, guild_id, technologies, role_p1_2023, role_p2_2023
from utils.intern_fetcher import fetch_api_intern
from utils.utils_departement import get_departement


async def send_jobslist(bot, ctx=None, loading_message=None):
    if ctx:
        guild = ctx.guild
        forum_channel_job = guild.get_channel(forum_channel_id)
    else:
        guild = bot.get_guild(guild_id)
        if guild is None:
            print("Guild not found")
            return
        forum_channel_job = guild.get_channel(forum_channel_id)

    if isinstance(forum_channel_job, discord.ForumChannel):
        available_tags = list(forum_channel_job.available_tags)
        # Obtenir les threads actifs et archivés existants
        active_threads = forum_channel_job.threads
        archived_threads = [
            thread
            async for thread in forum_channel_job.archived_threads(limit=100)
        ]

        all_threads = active_threads + archived_threads

        list_jobs, query_message, error = await fetch_api_intern(bot)

        """for offre in list_jobs:
            print(f"Job Apply Link: {offre['job_apply_link']}")
            print(f"Job Publisher: {offre['job_publisher']}")
            print("---")

        # Afficher le nombre total d'offres
        print(f"Total number of offers: {len(list_jobs)}")"""

        if error:
            if ctx:
                if loading_message:
                    embed_error = discord.Embed(
                        title="❌ Erreur de l'API",
                        description=f"{error}",
                        color=discord.Color.red()
                    )
                    embed_error.set_footer(text="Veuillez réessayer plus tard.")
                    await loading_message.edit(embed=embed_error)
                return  # Arrêter la fonction si la query n'est pas définie

        # Vérification si aucune query n'a été initialisée
        if "Aucune query n'a été définie" in query_message:
            if ctx:
                if loading_message:
                    embed_error = discord.Embed(
                        title="⚠️ Erreur : Query Non Initialisée",
                        description="Aucune query n'a été définie. Veuillez initialiser une query avec la commande `!setqueryIntern`.",
                        color=discord.Color.red()
                    )
                    embed_error.set_footer(text="Veuillez configurer une query pour continuer.")
                    await loading_message.edit(embed=embed_error)
                return  # Arrêter la fonction si la query n'est pas définie
            else:
                channel_id = 1257310056546963479  # Remplace par l'ID de ton channel
                channel = bot.get_channel(channel_id)
                if channel:
                    embed_error = discord.Embed(
                        title="🚫 Erreur Automatique",
                        description="La tâche automatique n'a pas pu s'exécuter car aucune query n'a été définie. Veuillez configurer une query avec `!setqueryIntern`.",
                        color=discord.Color.red()
                    )
                    await channel.send(embed=embed_error)
                return  # Arrêter la fonction si la query n'est pas définie

        await asyncio.sleep(1)

        verif = False

        if ctx:
            if loading_message:
                if not list_jobs:
                    embed_updated = discord.Embed(
                        title="🔍 Aucune Nouvelle Offre",
                        description="Aucune nouvelle offre d'emploi pour les alternants n'a été trouvée.",
                        color=discord.Color.greyple()
                    )
                    embed_updated.add_field(
                        name="Message de l'API",
                        value=query_message if query_message else "Aucune query n'a été définie.",
                        inline=False
                    )
                    embed_updated.set_footer(text="Vérifiez plus tard pour les nouvelles offres.")
                    await loading_message.edit(embed=embed_updated)

        all_jobs = list_jobs
        found_threads = []
        new_threads_created = False

        normandie_count = 0

        for job in all_jobs:
            title = job.get("job_title")
            company = job.get("employer_name")
            date = job.get("job_posted_at_datetime_utc")
            link = job.get("job_apply_link")
            city = job.get("job_city")
            publisher = job.get("job_publisher")
            description = job.get("job_description")
            if not city or city == "None":
                city = job.get("job_state")

            departement = get_departement(city)

            normandie = ["Calvados", "Eure", "Manche", "Orne", "Seine-Maritime"]

            # Vérification des mots interdits
            if contains_forbidden_words(company) or contains_forbidden_words(publisher):
                print(f"Offre ignorée : {company}, Mot(s) interdit(s) détecté(s).")
                if departement in normandie and job.get("job_state") != "IDF":
                    print("L'offre ignorée était de Normandie.")
                continue

            if title and link and company:
                # Extraire les technologies de la description
                extracted_techs = extract_technologies(description, technologies)
                extracted_techs = extract_technologies(title, technologies) + extracted_techs

                unique_techs = list(set(extracted_techs))
                # print(f"Techno extraite pour l'offre {title} : {unique_techs}")
                technologies_text = ", ".join(unique_techs) if unique_techs else "Aucune technologie spécifiée"

                # Si aucune technologie n'est trouvée, passer à l'offre suivante
                """
                if not unique_techs:
                    print(f"Aucune technologie trouvée pour l'offre {title}.")
                    continue
                """

                thread_title = f"{company} - {title}"

                # Chercher un thread existant avec le même titre
                existing_thread = None
                for thread in all_threads:
                    if thread.name == thread_title:
                        existing_thread = thread
                        found_threads.append(existing_thread)
                        break

                # Si un thread avec le même titre existe déjà, passe au suivant
                if existing_thread:
                    print("Thread found:", existing_thread.name)
                    continue

                if departement in normandie and job.get("job_state") != "IDF":
                    normandie_count += 1
                    print(f"Offre de Normandie comptée : {title}, {city}, de l'entreprise {company}")
                    thread_content = (
                        f"👋 Bonjour Apprenants <@{role_p1_2023}>, <@{role_p2_2023}>!\n\n"
                        f"🔎 Offre sur **{city}** chez **{company}**.\n"
                        f"📈 Poste recherché : **{title}**\n"
                        f"💻 Technologies : **{technologies_text}**\n"
                        f"🔗 Pour plus de détails et pour postuler, cliquez sur le lien : [Postuler]({link})"
                    )
                else:
                    thread_content = (
                        f"👋 Bonjour Apprenants !\n\n"
                        f"🔎 Offre d'alternance sur **{city}** chez **{company}**.\n"
                        f"📈 Poste recherché : **{title}**\n"
                        f"💻 Technologies : **{technologies_text}**\n"
                        f"🔗 Pour plus de détails et pour postuler, cliquez sur le lien : [Postuler]({link})"
                    )

                # Gérer les tags
                thread_tags = []
                for tech in extracted_techs[:5]:  # Limite de 5 tags
                    tag = next((t for t in available_tags if t.name.lower() == tech.lower()), None)
                    if not tag:
                        # Vérifier si le nombre de tags existants est inférieur à 20
                        if len(available_tags) < 20:
                            # Créer le tag si il n'existe pas
                            tag = await forum_channel_job.create_tag(name=tech)
                            available_tags.append(tag)
                        else:
                            # print(f"Nombre maximum de tags atteint. Impossible de créer le tag: {tech}")
                            continue
                    thread_tags.append(tag)

                # Créer le nouveau thread
                try:
                    thread = await forum_channel_job.create_thread(
                        name=thread_title, content=thread_content, applied_tags=thread_tags
                    )
                    new_threads_created = True
                    await asyncio.sleep(1)
                except discord.errors.HTTPException as e:
                    if e.code == 429:
                        print("Rate limited by Discord, will try again later.")
                        break

                await asyncio.sleep(1)

        # Vérifier si aucun nouveau thread n'a été créé
        if not new_threads_created:
            if loading_message:
                embed_updated = discord.Embed(
                    title="🔔 Aucune Nouvelle Offre",
                    description="Aucune nouvelle offre d'alternance n'a été trouvée.",
                    color=discord.Color.green()
                )
                embed_updated.add_field(
                    name="Message de l'API",
                    value=query_message if query_message else "Aucune query n'a été définie.",
                    inline=False
                )
                await loading_message.edit(embed=embed_updated)
        else:
            if loading_message:
                embed_updated = discord.Embed(
                    title="✅ Mise à Jour Terminée",
                    description=f"Toutes les nouvelles offres d'alternance ont été publiées avec succès.\nNombre d'offres pour Normandie: {normandie_count}",
                    color=discord.Color.blue()
                )
                embed_updated.add_field(
                    name="Message de l'API",
                    value=query_message if query_message else "Aucune query n'a été définie.",
                    inline=False
                )
                await loading_message.edit(embed=embed_updated)
            else:
                channel_id = 1257310056546963479
                channel = bot.get_channel(channel_id)
                if channel and normandie_count > 0:
                    embed_update = discord.Embed(
                        title="✅ Mise à Jour Terminée",
                        description=f"Nombre d'offres d'alternance pour la Normandie: {normandie_count}",
                        color=discord.Color.blue()
                    )
                    await channel.send(embed=embed_update)

    else:
        print("Le canal spécifié n'est pas un ForumChannel.")
        if loading_message:
            embed_updated = discord.Embed(
                title="❌ Erreur de Canal",
                description="Le canal spécifié n'est pas un ForumChannel.",
                color=discord.Color.red()
            )
            await loading_message.edit(embed=embed_updated)

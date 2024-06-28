import os
import discord
import json
import requests
import asyncio
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


def fetch_new_jobs():
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {
        "query": "Developer fullstack in france",
        "page": "1",
        "num_pages": "1",
        "date_posted": "all",
        "employment_types": "INTERN"
    }
    headers = {
        "x-rapidapi-key": "a8fbf570efmsh8342bf88927fc47p1a79c7jsn755be17fe9ae",
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        jobs = data.get('data', [])
        return jobs if isinstance(jobs, list) else []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs from new API: {e}")
        return []


# Fonction pour obtenir les offres d'emploi depuis l'API LinkedIn Jobs Search
def fetch_linkedin_jobs():
    url = "https://linkedin-jobs-search.p.rapidapi.com/"
    payload = {
        "search_terms": "Alternance_Développeur",
        "location": "Rouen, France",
        "page": "1",
        "employment_type": ["INTERN"]
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "a8fbf570efmsh8342bf88927fc47p1a79c7jsn755be17fe9ae",
        "X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    jobs = response.json()

    return jobs


# Fonction pour obtenir les offres d'emploi depuis l'API Indeed
def fetch_indeed_jobs():
    url = "https://indeed12.p.rapidapi.com/jobs/search"
    querystring = {
        "query": "alternant développeur",
        "location": "rouen",
        "page_id": "1",
        "locality": "fr",
        "fromage": "1",
        "radius": "50",
        "sort": "date"
    }
    headers = {
        "x-rapidapi-key": "9ebfc16424msh31785378b8b5536p1d17d6jsncc048dd648a3",
        "x-rapidapi-host": "indeed12.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        jobs = response.json().get('hits', [])
        return jobs if isinstance(jobs, list) else []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Indeed jobs: {e}")
        return []


async def send_joblist(ctx=None):
    forum_channel_id = 1245322710825832502  # ID du canal ForumChannel
    forum_channel = bot.get_channel(forum_channel_id)

    if isinstance(forum_channel, discord.ForumChannel):
        # Obtenir les threads actifs et archivés existants
        active_threads = forum_channel.threads
        archived_threads = [
            thread
            async for thread in forum_channel.archived_threads(limit=100)
        ]

        all_threads = active_threads + archived_threads

        # Récupérer les offres d'emploi depuis les API
        linkedin_jobs = fetch_linkedin_jobs()
        indeed_jobs = fetch_indeed_jobs()
        jSearch_jobs = fetch_new_jobs()

        # Fusionner les deux listes d'offres d'emploi
        all_jobs = linkedin_jobs + indeed_jobs

        all_new_jobs = jSearch_jobs

        for job in all_new_jobs:
            company = job.get('employer_name')
            title = job.get('job_title')
            link = job.get('job_apply_link')
            date = job.get('job_posted_at_datetime_utc')
            technologies = job.get('job_required_skills', 'Non spécifié')

            if title and link and company:
                thread_title = f"{company} - {title}"

                if date and link:
                    thread_content = f"Bonjour <@&1245022493371011135> ! Offre d'alternance chez **{company}** qui recherche un développeur **{title}** utilisant les technologies suivantes : **{technologies}**. Pour plus de détails et pour postuler, cliquez sur le lien : {link}"

                    # Chercher un thread existant avec le même titre
                    existing_thread = None
                    for thread in all_threads:
                        if thread.name == thread_title:
                            existing_thread = thread
                            break

                    # Si un thread avec le même titre existe déjà, passe au suivant
                    if existing_thread:
                        print("Thread found:", existing_thread.name)
                        continue

                    # Créer le nouveau thread
                    try:
                        thread = await forum_channel.create_thread(
                            name=thread_title, content=thread_content)
                    except discord.errors.HTTPException as e:
                        if e.code == 429:
                            print(
                                "Rate limited by Discord, will try again later."
                            )
                            break

                    # Pause pour éviter de dépasser les limites de taux
                    await asyncio.sleep(1)

                if ctx:
                    await ctx.send("Les offres d'emploi ont été mises à jour.")
            else:
                print("Le canal spécifié n'est pas un ForumChannel.")
                if ctx:
                    await ctx.send(
                        "Le canal spécifié n'est pas un ForumChannel.")

        for job in all_jobs:
            title = job.get("job_title") or job.get("title")
            company = job.get("company_name")
            date = job.get("posted_date") or job.get("formatted_relative_time")
            link = job.get("linkedin_job_url_cleaned"
                           ) or "https://fr.indeed.com" + job.get("link")
            technologies = job.get('skills', 'Non spécifié')
            if title and link and company:
                thread_title = f"{company} - {title}"

                if date and link:
                    thread_content = f"Bonjour <@&1245022493371011135> ! Offre d'alternance chez **{company}** qui recherche un développeur **{title}** utilisant les technologies suivantes : **{technologies}**. Pour plus de détails et pour postuler, cliquez sur le lien : {link}"

                    # Chercher un thread existant avec le même titre
                    existing_thread = None
                    for thread in all_threads:
                        if thread.name == thread_title:
                            existing_thread = thread
                            break

                    # Si un thread avec le même titre existe déjà, passe au suivant
                    if existing_thread:
                        print("Thread found:", existing_thread.name)
                        continue

                    # Créer le nouveau thread
                    try:
                        thread = await forum_channel.create_thread(
                            name=thread_title, content=thread_content)
                    except discord.errors.HTTPException as e:
                        if e.code == 429:
                            print(
                                "Rate limited by Discord, will try again later."
                            )
                            break

                    # Pause pour éviter de dépasser les limites de taux
                    await asyncio.sleep(1)
        if ctx:
            await ctx.send("Les offres d'emploi ont été mises à jour.")
    else:
        print("Le canal spécifié n'est pas un ForumChannel.")
        if ctx:
            await ctx.send("Le canal spécifié n'est pas un ForumChannel.")


@bot.event
async def on_ready():
    print('Bot is ready.')
    # Démarrage du scheduler pour exécuter la fonction send_joblist deux fois par jour
    scheduler.start()


# Scheduler pour exécuter la fonction send_joblist deux fois par jour
scheduler = AsyncIOScheduler()


@scheduler.scheduled_job("cron", hour=10, minute=0)  # Exécuter à 8h du matin
async def joblist_morning():
    await send_joblist()


@scheduler.scheduled_job("cron", hour=18, minute=0)  # Exécuter à 16h
async def joblist_evening():
    await send_joblist()


@bot.command(name='update_jobs')
async def update_jobs(ctx):
    await send_joblist()



## BOT AIDE POUR LES APPRENANTS 


# Remplacez selon le message et le rôle à donner pour les aides !
MESSAGE_ID = 1256205265401937960  # ID du message à surveiller
ROLE_ID = 1245022484902707243  # Remplacez par l'ID du rôle à attribuer


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == MESSAGE_ID:
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(ROLE_ID)
        member = guild.get_member(payload.user_id)

        if member and role:
            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(MESSAGE_ID)

            for reaction in message.reactions:
                if reaction.emoji == payload.emoji.name:
                    if reaction.count > 1:
                        await member.add_roles(role)
                        # Modifier le pseudo de l'utilisateur
                        new_nickname = f"🚨 {member.display_name}"
                        try:
                            await member.edit(nick=new_nickname)
                        except discord.Forbidden:
                            print(
                                f"Je n'ai pas la permission de changer le pseudo de {member}."
                            )

                        help_channel_id = 1245022636367675517 # Changer le cannel de destination
                        help_channel = bot.get_channel(help_channel_id)
                        if help_channel:
                            await help_channel.send(
                                f"<@{member.id}> a besoin d'aide.")
                        else:
                            print(
                                f"Le canal d'ID {help_channel_id} n'a pas été trouvé."
                            )

                        break


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == MESSAGE_ID:
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(ROLE_ID)
        member = guild.get_member(payload.user_id)

        if member and role:
            await member.remove_roles(role)
            # Restaurer le pseudo d'origine de l'utilisateur
            if member.display_name.startswith("🚨"):
                original_nickname = member.display_name.replace("🚨 ", "")
                try:
                    await member.edit(nick=original_nickname)
                except discord.Forbidden:
                    print(
                        f"Je n'ai pas la permission de changer le pseudo de {member}."
                    )
                    
            help_channel_id = 1245022636367675517 # Changer le cannel de destination
            help_channel = bot.get_channel(help_channel_id)
            if help_channel:
                async for message in help_channel.history(limit=None):
                    if f"<@{member.id}> a besoin d'aide." in message.content:
                        await message.delete()
                        break
            else:
                print(f"Le canal d'ID {help_channel_id} n'a pas été trouvé.")


token = os.environ['TOKEN']
bot.run(token)

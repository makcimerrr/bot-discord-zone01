from apscheduler.schedulers.asyncio import AsyncIOScheduler
from cogs.gestion_jobs import JobCog  # Assurez-vous que JobCog est importé

scheduler = AsyncIOScheduler()


async def joblist_morning():
    job_cog = JobCog()  # Instanciez votre cog
    await job_cog.send_joblist()  # Appelez la méthode send_joblist
    print("Updated jobs list auto 1!")


async def joblist_evening():
    job_cog = JobCog()  # Instanciez votre cog
    await job_cog.send_joblist()  # Appelez la méthode send_joblist
    print("Updated jobs list auto 2!")


@scheduler.scheduled_job("cron", hour=8, minute=0)  # Exécuter à 8h du matin
async def schedule_joblist_morning():
    await joblist_morning()


@scheduler.scheduled_job("cron", hour=14, minute=10)  # Exécuter à 14h
async def schedule_joblist_evening():
    await joblist_evening()


# Démarrer le scheduler
def start_scheduler():
    scheduler.start()

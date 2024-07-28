from apscheduler.schedulers.asyncio import AsyncIOScheduler

from cogs.gestion_jobs import JobCog
from cogs.gestion_cdi import CDICog

scheduler = AsyncIOScheduler()


async def joblist_morning(bot):
    job_cog = JobCog(bot)  # Instanciez votre cog
    await job_cog.send_joblist()  # Appelez la méthode send_joblist
    print("Updated jobs list auto 1!")


async def joblist_evening(bot):
    job_cog = JobCog(bot)  # Instanciez votre cog
    await job_cog.send_joblist()  # Appelez la méthode send_joblist
    print("Updated jobs list alternants auto 2!")


async def cdi_morning(bot):
    cdi_cog = CDICog(bot)  # Instanciez votre cog
    await cdi_cog.send_cdilist()  # Appelez la méthode send_joblist
    print("Updated jobs list auto 1!")


async def cdi_evening(bot):
    cdi_cog = CDICog(bot)  # Instanciez votre cog
    await cdi_cog.send_cdilist()  # Appelez la méthode send_joblist
    print("Updated jobs list cdi auto 2!")


def start_scheduler(bot):
    # Scheduler jobs with bot parameter
    @scheduler.scheduled_job("cron", hour=9, minute=0)  # Run at 9 AM
    async def schedule_joblist_morning():
        await joblist_morning(bot)
        await cdi_morning(bot)

    @scheduler.scheduled_job("cron", hour=18, minute=0)  # Run at 6 PM
    async def schedule_joblist_evening():
        await joblist_evening(bot)
        await cdi_evening(bot)

    scheduler.start()

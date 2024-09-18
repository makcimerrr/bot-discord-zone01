from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from utils.utils_internship import send_jobslist
from utils.utils_fulltime import send_cdilist

scheduler = AsyncIOScheduler()


async def joblist_morning(bot):
    await send_jobslist(bot)  # Appelez la méthode send_joblist
    print("Updated list internship auto 1!")


async def joblist_evening(bot):
    await send_jobslist(bot)  # Appelez la méthode send_joblist
    print("Updated list internship auto 2!")


async def cdi_morning(bot):
    await send_cdilist(bot)  # Appelez la méthode send_joblist
    print("Updated list full-time auto 1!")


async def cdi_evening(bot):
    await send_cdilist(bot)  # Appelez la méthode send_joblist
    print("Updated list full-time auto 2!")


def start_scheduler(bot):
    # Print the time of the scheduler start
    print(f"Scheduler started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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

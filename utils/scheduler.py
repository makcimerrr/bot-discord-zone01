import discord
import re
import locale
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger

from utils.utils_internship import send_jobslist
from utils.utils_fulltime import send_cdilist
from utils.progress_fetcher import fetch_progress
from utils.config_loader import config
from utils.timeline import fetch_and_send_progress
from utils.notifier import send_monthly_message

scheduler = AsyncIOScheduler()

# Définir la locale en français pour formater les mois en français
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    print("⚠️ Locale fr_FR.UTF-8 non disponible. Les mois seront affichés en anglais.")


async def joblist_morning(bot):
    await send_jobslist(bot)  # Appelez la méthode send_joblist
    print("Updated list internship auto 1!")


async def joblist_evening(bot):
    await send_jobslist(bot)  # Appelez la méthode send_joblist
    print("Updated list internship auto 2!")


async def cdi_morning(bot):
    await send_cdilist(bot)
    print("Updated list full-time auto 1!")


async def cdi_evening(bot):
    await send_cdilist(bot)
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

    @scheduler.scheduled_job("cron", hour=9, minute=0)  # Run at 9 AM
    async def schedule_fetch_progress_morning():
        await fetch_and_send_progress(bot)

    @scheduler.scheduled_job("cron", hour=18, minute=0)  # Run at 6 PM
    async def schedule_fetch_progress_evening():
        await fetch_and_send_progress(bot)

    @scheduler.scheduled_job(
        CronTrigger(day='1-7', day_of_week='mon', hour=14, minute=0)
    )
    async def monthly_task():
        await send_monthly_message(bot)

    scheduler.start()
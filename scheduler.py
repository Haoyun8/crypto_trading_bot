# scheduler.py

import schedule
import time
import asyncio
from logger import log_info
from trading import update_symbols

def weekly_job():
    log_info("Executing weekly symbol update job...")
    asyncio.run(update_symbols())

def start_scheduler():
    schedule.every(1).week.do(weekly_job)
    log_info(f"Scheduler started, job scheduled every week for symbol update.")

    while True:
        schedule.run_pending()
        time.sleep(1)


from django.conf.global_settings import TIME_ZONE
from .jobs import RoutineResultSchedule
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz


def start():
    scheduler = BackgroundScheduler(timezone=pytz.timezone(TIME_ZONE))
    scheduler.add_job(execute_schedule, CronTrigger.from_crontab('0 0 * * *'))
    scheduler.start()


def execute_schedule():
    schedule = RoutineResultSchedule()
    return schedule.run()


# cron.py
from django_cron import CronJobBase, Schedule
import logging

# Configure the logging settings
logging.basicConfig(filename='cron_job.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ClearUponDayEndCronJob(CronJobBase):
    from .views import clear_upon_day_end
    clear_upon_day_end()
    logging.info('Database cleared.')

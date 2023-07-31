# cron.py
from django_cron import CronJobBase, Schedule

class ClearUponDayEndCronJob(CronJobBase):
    RUN_EVERY_MIDNIGHT = Schedule(run_at_times=['00:00'])

    def job(self):
        from .views import clear_upon_day_end
        clear_upon_day_end()

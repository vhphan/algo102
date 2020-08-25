from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from data_providers.finnhub.cron.update_db import update_data_db
from data_providers.finnhub.cron.apply_filters import apply_the_filters
from data_providers.finnhub.get_data_finnhub import get_symbols


def task():
    get_symbols()
    update_data_db()
    apply_the_filters()


def schedule_tasks():
    # scheduler = BackgroundScheduler(daemon=True)
    scheduler_ = BlockingScheduler()
    scheduler_.add_job(task, 'cron', hour=5, minute=0)
    return scheduler_


if __name__ == '__main__':
    scheduler = schedule_tasks()
    scheduler.start()

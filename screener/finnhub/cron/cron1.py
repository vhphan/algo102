from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from screener.finnhub.cron.update_db import update_data_db
from screener.finnhub.cron.apply_filters import apply_the_filters


def task():
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

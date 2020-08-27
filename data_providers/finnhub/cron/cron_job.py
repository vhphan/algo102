from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

from data_providers.binance.get_squeeze_list import get_crypto_squeeze_list
from data_providers.finnhub.cron.update_db import update_data_db
from data_providers.finnhub.cron.apply_filters import apply_the_filters
from data_providers.finnhub.get_data_finnhub import get_symbols


def task1():
    get_symbols()
    update_data_db()
    apply_the_filters()


def task2():
    get_crypto_squeeze_list()


def schedule_tasks():
    # scheduler = BackgroundScheduler(daemon=True)
    bl_scheduler = BlockingScheduler()
    return bl_scheduler


def schedule_background_tasks():
    bg_scheduler = BackgroundScheduler()
    return bg_scheduler


if __name__ == '__main__':
    scheduler1 = schedule_tasks()
    scheduler1.add_job(task1, 'cron', hour=5, minute=0)
    scheduler1.start()
    # scheduler2 = schedule_background_tasks()
    # scheduler2.add_job(task2, 'cron', hour=5, minute=0)

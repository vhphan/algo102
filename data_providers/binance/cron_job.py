from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from data_providers.binance.get_all import get_all
from data_providers.binance.get_squeeze_list import get_crypto_squeeze_list


def task():
    get_all()
    get_crypto_squeeze_list()


def schedule_tasks():
    # scheduler = BackgroundScheduler(daemon=True)
    scheduler_ = BlockingScheduler()
    scheduler_.add_job(task, 'cron', hour=6, minute=0)
    return scheduler_


if __name__ == '__main__':
    scheduler = schedule_tasks()
    scheduler.start()

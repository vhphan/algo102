from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

from data_providers.finnhub.cron.apply_filters import apply_the_filters
from data_providers.finnhub.get_data_finnhub import get_symbols, update_data_db
from lib.my_email import send_eri_mail


def schedule_tasks():
    # scheduler = BackgroundScheduler(daemon=True)
    bl_scheduler = BlockingScheduler()
    return bl_scheduler


def schedule_background_tasks():
    bg_scheduler = BackgroundScheduler()
    return bg_scheduler


def cron_stocks():
    get_symbols()
    update_data_db()
    apply_the_filters()
    msg = "<p>cron stocks completed</p>"
    send_eri_mail(recipient='phanveehuen@gmail.com', message_=msg, subject='cron update')


if __name__ == '__main__':
    scheduler1 = schedule_tasks()
    scheduler1.add_job(cron_stocks, 'cron', hour=5, minute=0)
    scheduler1.start()
    # scheduler2 = schedule_background_tasks()
    # scheduler2.add_job(task2, 'cron', hour=5, minute=0)

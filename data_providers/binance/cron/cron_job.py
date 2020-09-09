from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from data_providers.binance.get_all import get_all
from data_providers.binance.get_squeeze_list import get_crypto_squeeze_list, save_top_coins
from lib.error_decorator import safe_run
from lib.my_email import send_eri_mail


@safe_run
def cron_crypto():
    print('running...cron #1')
    get_all()
    print('running...cron #2')
    save_top_coins()
    print('running...cron #3')
    get_crypto_squeeze_list()
    msg = "<p>cron crypto completed</p>"
    send_eri_mail(recipient='phanveehuen@gmail.com', message_=msg, subject='cron update')


def schedule_tasks():
    # scheduler = BackgroundScheduler(daemon=True)
    scheduler_ = BlockingScheduler()
    scheduler_.add_job(cron_crypto, 'cron', hour=12, minute=21)
    return scheduler_


if __name__ == '__main__':
    scheduler = schedule_tasks()
    scheduler.start()
    # cron_crypto()
# /home2/eproject/vee-h-phan.com/
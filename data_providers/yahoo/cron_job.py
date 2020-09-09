from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from data_providers.yahoo.get_all import main
from lib.error_decorator import safe_run
from lib.my_email import send_eri_mail


@safe_run
def cron_yahoo():
    main()
    msg = "<p>cron yahoo completed</p>"
    send_eri_mail(recipient='phanveehuen@gmail.com', message_=msg, subject='cron update')


def schedule_tasks():
    # scheduler = BackgroundScheduler(daemon=True)
    scheduler_ = BlockingScheduler()
    scheduler_.add_job(cron_yahoo, 'cron', hour=8, minute=21)
    return scheduler_


if __name__ == '__main__':
    scheduler = schedule_tasks()
    scheduler.start()

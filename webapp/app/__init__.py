from flask import Flask
from flask_mail import Message
from flask_wtf.csrf import CSRFProtect
from loguru import logger

# from data_providers.binance.cron_job import cron_crypto
from data_providers.binance.get_all import get_all
from data_providers.binance.get_squeeze_list import save_top_coins, get_crypto_squeeze_list
from data_providers.finnhub.cron.cron_job import cron_stocks
from lib.my_email import send_eri_mail
from .data_api.binance.views import bb
from my_flask_mail import mail
from .data_api.finnhub import fh
from .web import web
from .initialize import APP_PATH, today_str
# from .examples.eg001_embedded_signing import eg001
from webapp.app.views import core
from cache import cache
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

logger.add(f"{APP_PATH}/logs/ds2_{today_str}.log", rotation="1 MB", backtrace=True, diagnose=True)
session_path = "/tmp/python_recipe_sessions"

app = Flask(__name__, static_folder=None)
app.config.from_pyfile("config.py")
csrf = CSRFProtect(app)
cache.init_app(app)

# Register core
app.register_blueprint(core)
app.register_blueprint(fh)
app.register_blueprint(web)
app.register_blueprint(bb)

# app.register_blueprint(webhook)
# csrf.exempt(webhook)

# flask mail
mail.init_app(app)


def cron_test():
    msg = "<p>cron test msg</p>"
    send_eri_mail(recipient='phanveehuen@gmail.com', message_=msg, subject='cron update')


def cron_crypto():
    print('running...cron #1')
    get_all()
    print('running...cron #2')
    save_top_coins()
    print('running...cron #3')
    get_crypto_squeeze_list()
    msg = "<p>cron crypto completed</p>"
    mail_msg = Message(subject='SQUEEZED!', recipients=['phanveehuen@gmail.com'], html=msg)
    mail.connect()
    mail.send(mail_msg)


scheduler = BackgroundScheduler()
scheduler.add_job(cron_crypto, 'cron', hour=10, minute=5)  # daily cron at UTC 12:15 am in my local time
# scheduler.add_job(cron_stocks, 'cron', hour=4, minute=1)
scheduler.add_job(cron_test, 'cron', hour=14, minute=31)
# scheduler.add_job(cron_test, 'interval', minutes=2)
scheduler.start()

# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: scheduler.shutdown(wait=False))

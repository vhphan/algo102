from flask import Flask, session
from flask_mail import Message
from flask_wtf.csrf import CSRFProtect
from loguru import logger

from data_providers.finnhub.cron.apply_filters import apply_the_filters
from data_providers.finnhub.get_data_finnhub import get_symbols, update_data_db
from .data_api.binance.views import bb
from data_providers.binance.get_all import get_all
from data_providers.binance.get_squeeze_list import get_crypto_squeeze_list
from my_flask_mail import mail
from .data_api.finnhub import fh
from .web import web
from .initialize import APP_PATH, today_str
# from .examples.eg001_embedded_signing import eg001
from webapp.app.views import core
from cache import cache
from apscheduler.schedulers.background import BackgroundScheduler


def cron_crypto():
    print('running...cron #1')
    get_all()
    print('running...cron #2')
    get_crypto_squeeze_list()
    msg = "<p>cron crypto completed</p>"
    mail_msg = Message(subject='cron update', recipients=['phanveehuen@gmail.com'], html=msg)
    mail.connect()
    mail.send(mail_msg)


def cron_stocks():
    get_symbols()
    update_data_db()
    apply_the_filters()
    msg = "<p>cron stocks completed</p>"
    mail_msg = Message(subject='cron update', recipients=['phanveehuen@gmail.com'], html=msg)
    mail.connect()
    mail.send(mail_msg)


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(cron_crypto, 'cron', hour=13, minute='15')  # daily cron atUTC 12:15 am in my local time
scheduler.add_job(cron_stocks, 'cron', hour=5, minute='01')
scheduler.start()

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

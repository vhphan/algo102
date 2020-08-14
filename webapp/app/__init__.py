from flask import Flask, session
from flask_wtf.csrf import CSRFProtect
from loguru import logger

from .data_api.finnhub import fh
from .web import web
from .initialize import APP_PATH, today_str
# from .examples.eg001_embedded_signing import eg001
from webapp.app.views import core
from cache import cache

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

# app.register_blueprint(webhook)
# csrf.exempt(webhook)


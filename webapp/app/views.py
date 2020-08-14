"""Defines the home page route"""
from datetime import datetime

from flask import render_template, url_for, redirect, Blueprint, jsonify
from loguru import logger

core = Blueprint("core", __name__, template_folder='templates')


@core.route("/")
def index():
    # return render_template("home.html", title="Home - Python Code Examples")
    return f'<h2>Test message at {datetime.now()}</h2>'


@core.route("/index")
def r_index():
    return redirect(url_for("core.index"))


@core.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@core.app_errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

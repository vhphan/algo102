from flask import render_template, redirect, Blueprint, request, session

web = Blueprint("web", __name__,
                url_prefix='/web',
                template_folder='web_templates',
                static_folder='web_static')


@web.route('/')
def web_index():
    return 'hello web'
    # return render_template('screener.html')


@web.route('/ttm-squeeze')
def ttm_squeeze():
    return render_template('ttm-squeeze.html')


@web.route('/bbot')
def binance_bot():
    # return 'hello web'
    return render_template('binance_bot.html')


@web.route('/pattern')
def pattern():
    return render_template('pattern.html')


@web.route('/test')
def web_test():
    return 'hello test'


@web.route('/breakout')
def breakout():
    return render_template('breakout.html')
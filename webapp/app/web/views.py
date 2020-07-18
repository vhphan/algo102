from flask import render_template, redirect, Blueprint, request, session

web = Blueprint("web", __name__,
                url_prefix='/web',
                template_folder='web_templates',
                static_folder='web_static')


@web.route('/')
def web_index():
    # return 'hello web'
    return render_template('dashboard0.html')


@web.route('/test')
def web_test():
    return 'hello test'

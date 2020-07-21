from flask import Flask
from loguru import logger

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.errorhandler(500)
def somehandler(e):
    logger.critical(e.description)


if __name__ == '__main__':
    app.run()

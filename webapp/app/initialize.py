import os
import socket
from datetime import date, datetime
from pathlib import Path

from lib.mysql_db import EPortalDB

today_str = date.today().strftime('%Y%m%d')
today_time_str = datetime.now().strftime('%Y%m%d%H%M%S')
APP_PATH = Path(os.path.abspath(__file__)).parent.parent.parent  # /home2/eproject/veehuen/python/algo102

e_db = EPortalDB.Instance()

host_name = socket.gethostname()

if host_name == 'server.eprojecttrackers.com':
    host_url = 'https://cmeportal.eprojecttrackers.com'
    py_host_url = 'https://cmeportal.eprojecttrackers.com/ds2'
else:
    host_url = 'http://127.0.0.1/eportal3'
    py_host_url = 'http://127.0.0.1:5000'

if __name__ == '__main__':
    print(APP_PATH)

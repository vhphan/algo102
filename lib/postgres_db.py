from datetime import datetime, date
import os
from pathlib import Path

from lib.db88 import DB88
from private.keys import ep_fx_keys
from lib.singleton import Singleton

dbc = ep_fx_keys
dbc['port'] = 5432

today_str = date.today().strftime('%Y%m%d')
today_time_str = datetime.now().strftime('%Y%m%d%H%M%S')

current_path = Path(os.path.abspath(__file__)).parent


@Singleton
class EPortalPGDB(DB88):
    def __init__(self):
        super().__init__(db_con=dbc, db_type='postgres')


if __name__ == '__main__':
    c1 = EPortalPGDB.Instance()
    sql = "SELECT * FROM eproject_fx.public.btcusdt LIMIT 5"
    df = c1.query_df(sql)
    print(df)

    # c2 = EPortalDB.Instance()
    #
    # print("Id of c1 : {}".format(str(id(c1))))
    # print("Id of c2 : {}".format(str(id(c1))))
    #
    # print("c1 is c2 ? " + str(c1 is c2))

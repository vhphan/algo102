import MySQLdb
import psycopg2
from loguru import logger
import pandas as pd
from sqlalchemy import text, create_engine

from lib.error_decorator import safe_run


class DB88(object):

    def __init__(self, db_con, db_type='mysql'):
        self.db_type = db_type
        try:

            if db_type == 'mysql':
                self._conn = MySQLdb.connect(**db_con, charset='utf8')
                self.engine = create_engine(
                    f"mysql://{db_con['user']}:{db_con['passwd']}@{db_con['host']}:{db_con['port']}/{db_con['db']}?charset=utf8mb4",
                    echo=False)

            elif db_type == 'postgres':
                db_con['database'] = db_con.pop('db')
                self._conn = psycopg2.connect(**db_con)

                # dict(
                #     ep_fx=f"postgresql://{ep_fx_keys['user']}:{ep_fx_keys['password']}@{ep_fx_keys['host']}:5432/{ep_fx_keys['db']}")

                self.engine = create_engine(
                    f"postgresql://{db_con['user']}:{db_con['password']}@{db_con['host']}:{db_con['port']}/{db_con['database']}",
                    echo=False)

        except Exception as e:
            print(e.__repr__())

        self._cursor = self._conn.cursor()
        if db_type == 'mysql':
            self.execute(sql_query="SET session wait_timeout=300")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    def __str__(self):
        return self._conn

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql_query, params=None):
        return self.cursor.execute(sql_query, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    # @retry(Exception, tries=5)
    @safe_run
    def query(self, sql_query, params=None, return_dict=False):
        try:
            if self._conn is None:
                self.__init__()
            else:
                if self.db_type == 'mysql':
                    self._conn.ping(True)

            ex_result = self.cursor.execute(sql_query, params or ())
            if sql_query.lower().split()[0] in ['replace', 'update', 'insert', 'delete']:
                self.commit()
                return ex_result
        except Exception as e:
            logger.debug(f'{str(e)} : {sql_query}')
            return None

        if return_dict:
            columns = [col[0] for col in self.cursor.description]
            rows = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            return rows
        return self.cursor.fetchall()

    @safe_run
    def queries(self, sql_list: list):
        if self._conn is None:
            self.__init__()
        else:
            self._conn.ping(True)
        for q in sql_list:
            self.cursor.execute(q)
        self.commit()
        return True

    @safe_run
    def query_df(self, sql_query):
        return pd.read_sql(text(sql_query), self.engine)

    @safe_run
    def df_to_db(self, df, **kwargs):
        df.to_sql(**kwargs, con=self.engine)

import socket

from lib.db88 import DB88
from lib.singleton import Singleton

host_name = socket.gethostname()

# uri = 'localhost' if host_name == 'server.eprojecttrackers.com' else '220.158.200.19'
uri = 'localhost'

# port = 3306
port = 3306 if host_name == 'server.eprojecttrackers.com' else 3307


@Singleton
class EPortalDB(DB88):
    def __init__(self):
        dbc = dict(host=uri, user="eproject_root", passwd="@ssw0rd89!", db="eproject_cm", port=port)
        super().__init__(db_con=dbc, db_type='mysql')


if __name__ == '__main__':
    c1 = EPortalDB.Instance()
    sql = "SELECT * FROM eproject_cm.tblsitedocument LIMIT 5"
    df = c1.query_df(sql)
    print(df)

    # c2 = EPortalDB.Instance()
    #
    # print("Id of c1 : {}".format(str(id(c1))))
    # print("Id of c2 : {}".format(str(id(c1))))
    #
    # print("c1 is c2 ? " + str(c1 is c2))

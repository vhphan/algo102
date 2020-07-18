import pandas as pd
from sqlalchemy import create_engine, text


if __name__ == '__main__':
    sql = "SELECT * FROM eproject_fx.btcusdt"
    df
import time as t
import pandas as pd
from sqlalchemy import create_engine
from config import environ

from pybittrex.client import Client

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 500)


def db_conection(file_name, table_name):

    DATABASE_CREDENTIALS = dict(
        database=environ.get('DATABASE_NAME', 'postgres'),
        user=environ.get('DATABASE_USER', 'postgres'),
        password=environ.get('DATABASE_PASSWORD', ''),
        host=environ.get('DATABASE_HOST', 'localhost'),
        port=environ.get('DATABASE_PORT', '5432')
    )

    DATABASE_URL = 'postgres://{user}:{password}@{host}:{port}/{database}'.format(**DATABASE_CREDENTIALS)
    engine = create_engine(DATABASE_URL)

    # read table and csv

    d = pd.read_sql_table(table_name, engine, schema='public')

    print("\nConnected to the {} table".format(table_name))

    # upload file to table

    file_name.to_sql(con=engine, name=table_name, if_exists='append', index=False, schema='public')

    # Eliminate duplicate fields

    conn = engine.connect()
    trans = conn.begin()
    conn.execute('''SELECT dedup_market_history()''')
    trans.commit()
    conn.close()

    return print(d)


def market_history(market):

    c = Client(api_key='abc', api_secret='123')

    # ----------------------------- Getting Data ----------------------------- #

    dfm = pd.DataFrame({})

    dfm.reset_index()
    hist = c.get_market_history(market).json()['result']

    df = pd.DataFrame(hist)

    df.rename(columns={'Id': 'market_id', 'OrderType': 'ordertype',
                       'Price': 'price', 'Quantity': 'quantity',
                       'TimeStamp': 'timestamp', 'Total': 'total'}, inplace=True)

    df = df.drop(['FillType', 'Uuid'], axis=1)

    dfm = dfm.append(df)

    dfm.drop_duplicates("market_id", keep="first", inplace=True)

    return dfm


while True:

    dfm = market_history(market='USD-BTC')
    db_conection(file_name=dfm, table_name='market_history')
    t.sleep(60)

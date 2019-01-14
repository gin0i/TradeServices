import pandas as pd
from sqlalchemy import create_engine
from config import postgre

engine = create_engine('postgresql+psycopg2://'+postgre.user+':'+postgre.password+'@'+postgre.db, pool_recycle=3600)


def save(pdf, name, index_name):
    store_in_db(pdf, name, index_name, engine)


def store_in_db(pdf, name, index_name, engine):
    pdf.reset_index(level=0, inplace=True)
    pdf = pdf.rename(columns={index_name: 'DateTime'})
    pdf['DateTime'] = pdf['DateTime'].values.astype('datetime64')
    pdf.to_sql(name, con=engine, if_exists='replace')


def str_to_datetime(input_str):
    return pd.to_datetime(input_str, utc=True)

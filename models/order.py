from sqlalchemy import Column, Integer, String, DateTime, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config import postgre

engine = create_engine('postgresql+psycopg2://'+postgre.user+':'+postgre.password+'@'+postgre.db, pool_recycle=3600)
Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    exchange = Column(String)
    symbol = Column(String)
    fee = Column(Float)
    side = Column(String)
    price = Column(String)
    datetime = Column(DateTime)
    type = Column(String)
    cost = Column(Float)
    amount = Column(Float)
    filled = Column(Float)
    average = Column(Float)
    remaining = Column(Float)
    status = Column(String)
    timestamp = Column(TIMESTAMP)

    def __repr__(self):
        return "<Position(symbol='%s', amount='%s', price='%s', datetime='%s', type='%s')>" % (self.symbol, self.amount, self.price, self.datetime, self.type)


Base.metadata.create_all(engine)
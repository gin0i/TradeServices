from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config import postgre

engine = create_engine('postgresql+psycopg2://'+postgre.user+':'+postgre.password+'@'+postgre.db, pool_recycle=3600)
Base = declarative_base()


class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    exchange = Column(String)
    side = Column(String)
    price = Column(Float)
    datetime = Column(DateTime)
    type = Column(String)
    cost = Column(Float)
    amount = Column(Float)

    def __repr__(self):
        return "<Position(symbol='%s', amount='%s', price='%s', datetime='%s', type='%s')>" % (self.symbol, self.amount, self.price, self.datetime, self.type)


Base.metadata.create_all(engine)
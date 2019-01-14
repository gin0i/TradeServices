from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config import postgre

engine = create_engine('postgresql+psycopg2://'+postgre.user+':'+postgre.password+'@'+postgre.db, pool_recycle=3600)
Base = declarative_base()


class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    asset = Column(String)
    exchange = Column(String)
    free = Column(Float)
    total = Column(Float)
    used = Column(Float)
    date = Column(DateTime)

    def __repr__(self):
        return "<Position(asset='%s', free='%s', date='%s')>" % (self.asset, self.free, self.date)


Base.metadata.create_all(engine)
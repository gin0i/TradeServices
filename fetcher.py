import sched, time
import threading
from datetime import datetime
from models import position, trade
from random import random
import ccxt


class KrakenFetcher(object):
    def __init__(self, symbol, session, credentials):
        self.symbol = symbol
        self.session = session
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.event = None
        self.kraken = ccxt.kraken(credentials)

    def startup(self):
        self.event = self.scheduler.enter(1, 1, self.work_wrapper)
        threading.Thread(target=self.scheduler.run).start()
        return "started"

    def stop(self):
        try:
            self.scheduler.cancel(self.event)
        except ValueError:
            pass
        return "stopped"

    def work_wrapper(self):
        self.work()
        self.event = self.scheduler.enter(10, 1, self.work_wrapper)

    def get_positions(self):
        date = datetime.now()
        snapshot = self.kraken.fetch_balance()
        positions_raw = [(asset, float(v.get('free')), float(v.get('total')), float(v.get('used'))) for asset, v in snapshot.items() if
                     asset not in ['free', 'used', 'total', 'info']]
        return [position.Position(asset=pos[0], free=(random()+10 * 100), total=pos[2], used=pos[3], date=date, exchange='kraken') for pos in positions_raw]

    def work(self):
        positions = self.get_positions()
        trades = self.get_trades(self.symbol)
        purged = self.purge_trades(trades)
        [self.insert_objects(pack) for pack in [positions, purged]]

    def insert_objects(self, objects):
        [self.session.add(obj) for obj in objects]
        self.session.commit()

    def purge_trades(self, trades):
        purged = []
        for tr in trades:
            found = self.session.query(trade.Trade).filter(trade.Trade.symbol == self.symbol).filter(trade.Trade.datetime == tr.datetime).filter(trade.Trade.price == tr.price).first()
            if found is None:
                purged.append(tr)
        return purged

    def get_orders(self):
        closed_orders = self.kraken.fetch_closed_orders()
        open_orders = self.kraken.fetch_open_orders()
        return open_orders, closed_orders

    def get_trades(self, symbol):
        snapshot = self.kraken.fetch_trades(symbol)
        trades_raw = [(v.get('side'), float(v.get('price')), v.get('datetime'), v.get('type'), float(v.get('cost')), float(v.get('amount'))) for v in
                         snapshot]
        return [trade.Trade(symbol=symbol, side=tr[0], price=tr[1], datetime=tr[2], type=tr[3], cost=tr[4], amount=tr[5], exchange='kraken') for tr in trades_raw]
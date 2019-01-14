from flask import request, Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import postgre, exchange_api_keys
import fetcher

app = Flask(__name__)
engine = create_engine('postgresql+psycopg2://'+postgre.user+':'+postgre.password+'@'+postgre.db, pool_recycle=3600)
Session = sessionmaker(bind=engine)
session = Session()
fetchers = {}


def get_symbol_from_request(request):
    return request.form['symbol']


@app.route('/fetcher/kraken/start', methods=['POST'])
def start_fetching_kraken():
    assert request.method == 'POST'
    symbol = get_symbol_from_request(request)
    fetchers[symbol] = fetcher.KrakenFetcher(symbol, session, exchange_api_keys['kraken'])
    return fetchers[symbol].startup()


@app.route('/fetcher/kraken/stop', methods=['POST'])
def stop_fetching_kraken():
    assert request.method == 'POST'
    symbol = get_symbol_from_request(request)
    return fetchers[symbol].stop()
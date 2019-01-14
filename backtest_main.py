from flask import request, Flask
import backtest_utils as butils
import pandas_utils as putils

app = Flask(__name__)


def get_period_bounds(request):
    begin_str = str(request.form['begin'])
    begin = putils.str_to_datetime(begin_str)
    end_str = str(request.form['end'])
    end = putils.str_to_datetime(end_str)
    return begin, end


def get_capital(request):
    return int(request.form['capital'])


@app.route('/backtest/start', methods=['POST'])
def start_backtest():
    assert request.method == 'POST'
    begin, end = get_period_bounds(request)
    capital = get_capital(request)
    base_currency = request.form.get('base_currency')
    frequency = request.form.get('frequency')
    exchange = request.form.get('exchange')
    return butils.launch(begin, end, capital, base_currency, frequency, exchange)

from logbook import Logger
import strategy
from catalyst import run_algorithm


NAMESPACE = 'current_strategy'
log = Logger(NAMESPACE)


def launch(begin, end, capital, currency='btc', frequency='minute', exchange='bitfinex'):
    initialize_func = strategy.initialize
    run_algorithm(
            capital_base=capital,
            data_frequency=frequency,
            initialize=initialize_func,
            handle_data=strategy.handle_data,
            analyze=strategy.analyze,
            exchange_name=exchange,
            algo_namespace=NAMESPACE,
            quote_currency=currency,
            start=begin,
            end=end,
        )
    return 'OK'

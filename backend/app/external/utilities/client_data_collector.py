'''
This module is desgined to collect data from the backedend before being sent to
the frontend to be displayed in the UI. We use cross exchange arbitrage to get data
on the arbotrage across all exchanges and fiat currencies for a given cryptocurrency.
We also use the fee calculator to get the fees for buying and selling cryptocurrencies
on different exchanges.
'''

import sys
import os

# Add the root directory of your project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))


from app.external.utilities.cross_exchange_fiat_arbitrage import CrossExchangeFiatArbitrage
from app.external.utilities.fee_calc import FeeCalculator

class DataCollector:
    """Collects data from the backend and sends it to the frontend"""
    def __init__(self, price_data, exchange_rates):
        self.price_data = price_data
        self.exchange_rates = exchange_rates
        self.cross_exchange_arbitrage = CrossExchangeFiatArbitrage(price_data, exchange_rates)
    
    def get_arbitrage_data(self):
        """Get the arbitrage data from the cross exchange arbitrage class"""
        arbitrage_data = self.cross_exchange_arbitrage.find_lowest_and_highest_price()
        lowest_price = arbitrage_data['lowest_price']
        lowest_price_exchange = arbitrage_data['lowest_price_exchange'][1].lower()
        highest_price = arbitrage_data['highest_price']
        highest_price_exchange = arbitrage_data['highest_price_exchange'][1].lower()
        crypto = arbitrage_data['lowest_price_exchange'][0]
        buy_currency = arbitrage_data['lowest_price_exchange'][2]
        sell_currency = arbitrage_data['highest_price_exchange'][2]
        # fee_calculator = FeeCalculator(
        #     exchange_buy=lowest_price_exchange,
        #     exchange_sell=highest_price_exchange,
        #     crypto=crypto,
        #     crypto_amount=1,
        #     crypto_price_buy=lowest_price,
        #     crypto_price_sell=highest_price,
        #     currency_withdrawal="USD",
        #     withdrawal_method="SWIFT"
        # )
        # # Calculate fees
        # fees = fee_calculator.calculate_fees()
        # total_fees = fees['total_fees']
        # arbitrage = fees['price arbitrage']
        # return {    
        #     'lowest_price': round(lowest_price, 2),
        #     'lowest_price_exchange': lowest_price_exchange,
        #     'highest_price': round(highest_price, 2),
        #     'highest_price_exchange': highest_price_exchange,
        #     'crypto': crypto,
        #     'buy_currency': buy_currency,
        #     'sell_currency': sell_currency,
        #     'total_fees': round(total_fees, 2),
        #     'arbitrage': round(arbitrage, 2),
        #     'profit': f"${round(arbitrage - total_fees, 2)}"
        # }
    
# Example usage
if __name__ == "__main__":
    # Example price data
    price_data= {
        'BTC': {
            'COINBASE': {
                'USD': {'price': 50000.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'EUR': {'price': 45000.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'GBP': {'price': 40000.0, 'timestamp': '2023-10-01T00:00:00Z'}
            },
            'BINANCE': {
                'USD': {'price': 50500.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'EUR': {'price': 45500.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'GBP': {'price': 40500.0, 'timestamp': '2023-10-01T00:00:00Z'}
            },
            # 'KRAKEN': {
            #     'USD': {'price': 50200.0, 'timestamp': '2023-10-01T00:00:00Z'},
            #     'EUR': {'price': 45200.0, 'timestamp': '2023-10-01T00:00:00Z'},
            #     'GBP': {'price': 40200.0, 'timestamp': '2023-10-01T00:00:00Z'}
            # },
            # 'GEMINI': {
            #     'USD': {'price': 50100.0, 'timestamp': '2023-10-01T00:00:00Z'},
            #     'EUR': {'price': 45100.0, 'timestamp': '2023-10-01T00:00:00Z'},
            #     'GBP': {'price': 40100.0, 'timestamp': '2023-10-01T00:00:00Z'}
            # },
            # 'BITSTAMP': {
            #     'USD': {'price': 50300.0, 'timestamp': '2023-10-01T00:00:00Z'},
            #     'EUR': {'price': 45300.0, 'timestamp': '2023-10-01T00:00:00Z'},
            #     'GBP': {'price': 40300.0, 'timestamp': '2023-10-01T00:00:00Z'}
            # },
            # 'HUOBI': {
            #     'USD': {'price': 50400.0, 'timestamp': '2023-10-01T00:00:00Z'},
            #     'EUR': {'price': 45400.0, 'timestamp': '2023-10-01T00:00:00Z'},
            #     'GBP': {'price': 40400.0, 'timestamp': '2023-10-01T00:00:00Z'}
            # },
            # 'OKEX': {
            #     'USD': {'price': 50600.0, 'timestamp': '2023-10-01T00:00:00Z'},
            #     'EUR': {'price': 45600.0, 'timestamp': '2023-10-01T00:00:00Z'},
            #     'GBP': {'price': 40600.0, 'timestamp': '2023-10-01T00:00:00Z'}
            # }
        }
    }

    # Example exchange rates
    exchange_rates = {
        'USD': 1.0,
        'EUR': 1.1,  # 1 EUR = 1.1 USD
        'GBP': 1.3   # 1 GBP = 1.3 USD
    }
    data_collector = DataCollector(price_data, exchange_rates)
    arbitrage_data = data_collector.get_arbitrage_data()
    print(arbitrage_data)

    

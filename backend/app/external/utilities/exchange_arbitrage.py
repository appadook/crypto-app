'''
this module is used to calculate the arbitrage within a singular exchange and their different fiat currencies, providing us
with the best arbitrage opportunity within a single exchnage and given exchage rates and fiat prices for a cryptocurrency.
'''

import sys
import os
from typing import Dict


# Add the root directory of your project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from app.types.price_data_types import PriceDataType

class ExchangeArbitrage:
    def __init__(self, price_data: PriceDataType, exchange_rates: Dict[str, float]):
        self.price_data = price_data
        self.exchange_rates = exchange_rates
    
    def find_lowest_and_highest_nominal_price(self):
        lowest_price = float('inf')
        lowest_price_exchange = None
        highest_price = float('-inf')
        highest_price_exchange = None
        for crypto, exchanges in self.price_data.items():
            for exchange, currencies in exchanges.items():
                for currency, data in currencies.items():
                    price_in_usd = data['price'] * self.exchange_rates[currency]
                    if price_in_usd < lowest_price:
                        lowest_price = price_in_usd
                        lowest_price_exchange = (crypto, exchange, currency)
                    if price_in_usd > highest_price:
                        highest_price = price_in_usd
                        highest_price_exchange = (crypto, exchange, currency)
        return {
            'lowest_price': lowest_price,
            'lowest_price_exchange': lowest_price_exchange,
            'highest_price': highest_price,
            'highest_price_exchange': highest_price_exchange
        }
    
    def display_arbitrage_opportunity(self):
        result = self.find_lowest_and_highest_nominal_price()
        print(f"Lowest price: {result['lowest_price']:.2f} USD at {result['lowest_price_exchange'][1]} in {result['lowest_price_exchange'][2]} for {result['lowest_price_exchange'][0]}")
        print(f"Highest price: {result['highest_price']:.2f} USD at {result['highest_price_exchange'][1]} in {result['highest_price_exchange'][2]} for {result['highest_price_exchange'][0]}")

    
# Example usage
if __name__ == "__main__":
    # Example price data
    price_data: PriceDataType = {
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
            'KRAKEN': {
                'USD': {'price': 50200.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'EUR': {'price': 45200.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'GBP': {'price': 40200.0, 'timestamp': '2023-10-01T00:00:00Z'}
            },
            'GEMINI': {
                'USD': {'price': 50100.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'EUR': {'price': 45100.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'GBP': {'price': 40100.0, 'timestamp': '2023-10-01T00:00:00Z'}
            },
            'BITSTAMP': {
                'USD': {'price': 50300.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'EUR': {'price': 45300.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'GBP': {'price': 40300.0, 'timestamp': '2023-10-01T00:00:00Z'}
            },
            'HUOBI': {
                'USD': {'price': 50400.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'EUR': {'price': 45400.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'GBP': {'price': 40400.0, 'timestamp': '2023-10-01T00:00:00Z'}
            },
            'OKEX': {
                'USD': {'price': 50600.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'EUR': {'price': 45600.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'GBP': {'price': 40600.0, 'timestamp': '2023-10-01T00:00:00Z'}
            }
        }
    }

    # Example exchange rates
    exchange_rates = {
        'USD': 1.0,
        'EUR': 1.1,  # 1 EUR = 1.1 USD
        'GBP': 1.3   # 1 GBP = 1.3 USD
    }

    arbitrage = ExchangeArbitrage(price_data, exchange_rates)
    arbitrage.display_arbitrage_opportunity()
    


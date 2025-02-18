'''
This module contains functions to find the lowest and highest price of a cryptocurrency across all different
exchanges and fiat currencies.
The output indicates the user where the lowest nominal price is and where the highest nominal price is, so
that the user can take advantage of arbitrage opportunities by buying in one exchange in one fiat currency and selling
on another exchange in another fiat currency.
DOUBLE ARBITRAGE
'''
import sys
import os
from typing import Dict, TypedDict


# Add the root directory of your project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from app.types.price_data_types import PriceDataType

class ExchangeRateData(TypedDict):
    rate: float
    timestamp: str

class CrossExchangeFiatArbitrage:
    def __init__(self, price_data: PriceDataType, exchange_rates: Dict[str, ExchangeRateData]):
        self.price_data = price_data
        self.exchange_rates = exchange_rates

    def find_lowest_and_highest_price(self):
        lowest_price = float('inf')
        lowest_price_exchange = None
        highest_price = float('-inf')
        highest_price_exchange = None

        # Process one crypto at a time
        for crypto, exchanges in self.price_data.items():
            # Reset for each cryptocurrency
            crypto_lowest_price = float('inf')
            crypto_lowest_exchange = None
            crypto_highest_price = float('-inf')
            crypto_highest_exchange = None

            # Only process the current cryptocurrency's data
            for exchange, currencies in exchanges.items():
                for currency, data in currencies.items():
                    try:
                        # Convert price to float
                        price = float(data['price'])
                        
                        # Handle exchange rates
                        if currency == 'USD':
                            rate = 1.0
                        else:
                            # Get exchange rate from dictionary structure
                            exchange_rate_data = self.exchange_rates.get(currency)
                            if not exchange_rate_data or not isinstance(exchange_rate_data, dict):
                                print(f"Missing or invalid exchange rate data for {currency}")
                                continue
                            
                            rate = exchange_rate_data.get('rate')
                            if rate is None or not isinstance(rate, (int, float)):
                                print(f"Exchange rate for {currency} is None or invalid")
                                continue
                        

                        # Calculate price in USD
                        price_in_usd = price * rate
                        
                        if price_in_usd < crypto_lowest_price:
                            crypto_lowest_price = price_in_usd
                            crypto_lowest_exchange = (crypto, exchange, currency)
                        if price_in_usd > crypto_highest_price:
                            crypto_highest_price = price_in_usd
                            crypto_highest_exchange = (crypto, exchange, currency)
                    except (ValueError, TypeError) as e:
                        print(f"Error processing price data: {e}, price: {data.get('price')}, currency: {currency}")
                        continue

            # If we found both a lowest and highest price for this crypto
            if crypto_lowest_exchange and crypto_highest_exchange:
                # Only update if this crypto has a better spread
                current_spread = (crypto_highest_price - crypto_lowest_price) / crypto_lowest_price
                best_spread = (highest_price - lowest_price) / lowest_price if lowest_price != float('inf') else 0
                
                if current_spread > best_spread:
                    lowest_price = crypto_lowest_price
                    lowest_price_exchange = crypto_lowest_exchange
                    highest_price = crypto_highest_price
                    highest_price_exchange = crypto_highest_exchange

        # Return the best arbitrage opportunity found
        if lowest_price_exchange and highest_price_exchange:
            return {
                'lowest_price': lowest_price,
                'lowest_price_exchange': lowest_price_exchange,
                'highest_price': highest_price,
                'highest_price_exchange': highest_price_exchange
            }
        else:
            return None  # Return None if no valid arbitrage opportunity found

    def display_arbitrage_opportunity(self):
        result = self.find_lowest_and_highest_price()
        if result:
            print(f"Lowest price: {result['lowest_price']} USD at {result['lowest_price_exchange'][1]} in {result['lowest_price_exchange'][2]} for {result['lowest_price_exchange'][0]}")
            print(f"Highest price: {result['highest_price']} USD at {result['highest_price_exchange'][1]} in {result['highest_price_exchange'][2]} for {result['highest_price_exchange'][0]}")
        else:
            print("No valid arbitrage opportunity found.")


# Example usage
if __name__ == "__main__":
    # Example timestamp
    EXAMPLE_TIMESTAMP = '2023-10-01T00:00:00Z'
    
    # Example exchange rates with correct structure
    exchange_rates = {
        'USD': {'rate': 1.0, 'timestamp': EXAMPLE_TIMESTAMP},
        'EUR': {'rate': 1.1, 'timestamp': EXAMPLE_TIMESTAMP},  # 1 EUR = 1.1 USD
        'GBP': {'rate': 1.3, 'timestamp': EXAMPLE_TIMESTAMP}   # 1 GBP = 1.3 USD
    }

    # Example price data
    price_data: PriceDataType = {
        'BTC': {
            'COINBASE': {
                'USD': {'price': 50000.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'EUR': {'price': 45000.0, 'timestamp': '2023-10-01T00:00:00Z'},
                'GBP': {'price': 4000.0, 'timestamp': '2023-10-01T00:00:00Z'}
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

    arbitrage = CrossExchangeFiatArbitrage(price_data, exchange_rates)
    arbitrage.display_arbitrage_opportunity()

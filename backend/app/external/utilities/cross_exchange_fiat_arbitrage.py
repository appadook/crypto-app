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
from typing import Dict, TypedDict, List


# Add the root directory of your project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from app.types.price_data_types import PriceDataType

class ExchangeRateData(TypedDict):
    rate: float
    timestamp: str

class ArbitrageOpportunity(TypedDict):
    crypto: str
    lowest_price: float
    lowest_price_exchange: tuple
    highest_price: float
    highest_price_exchange: tuple
    spread: float

class CrossExchangeFiatArbitrage:
    def __init__(self, price_data: PriceDataType, exchange_rates: Dict[str, ExchangeRateData]):
        self.price_data = price_data
        self.exchange_rates = exchange_rates

    def find_lowest_and_highest_price(self) -> List[ArbitrageOpportunity]:
        opportunities: List[ArbitrageOpportunity] = []

        # Process each cryptocurrency
        for crypto, exchanges in self.price_data.items():
            crypto_lowest_price = float('inf')
            crypto_lowest_exchange = None
            crypto_highest_price = float('-inf')
            crypto_highest_exchange = None

            for exchange, currencies in exchanges.items():
                for currency, data in currencies.items():
                    try:
                        # Convert price to float
                        price = float(data['price'])
                        
                        # Handle exchange rates
                        if currency == 'USD':
                            rate = 1.0
                        else:
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
                spread = (crypto_highest_price - crypto_lowest_price) / crypto_lowest_price
                
                # Only add opportunities with a positive spread
                if spread > 0:
                    opportunities.append({
                        'crypto': crypto,
                        'lowest_price': crypto_lowest_price,
                        'lowest_price_exchange': crypto_lowest_exchange,
                        'highest_price': crypto_highest_price,
                        'highest_price_exchange': crypto_highest_exchange,
                        'spread': spread
                    })

        # Sort opportunities by spread in descending order
        opportunities.sort(key=lambda x: x['spread'], reverse=True)
        return opportunities

    def display_arbitrage_opportunities(self):
        opportunities = self.find_lowest_and_highest_price()
        if opportunities:
            for opp in opportunities:
                print(f"\nCryptocurrency: {opp['crypto']}")
                print(f"Lowest price: {opp['lowest_price']} USD at {opp['lowest_price_exchange'][1]} in {opp['lowest_price_exchange'][2]}")
                print(f"Highest price: {opp['highest_price']} USD at {opp['highest_price_exchange'][1]} in {opp['highest_price_exchange'][2]}")
                print(f"Spread: {opp['spread']*100:.2f}%")
        else:
            print("No valid arbitrage opportunities found.")


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
    arbitrage.display_arbitrage_opportunities()

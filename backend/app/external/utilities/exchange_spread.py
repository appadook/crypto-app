'''
This class is used to track the highest and lowest prices of all our cryptocurrencies across different exchanges.
returns a dictionary of the highest and lowest prices for each crypto and fiat pair, or displaying
the spread between the highest and lowest prices.
'''
import sys
import os

# Add the root directory of your project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from app.types.price_data_types import PriceDataType

class ExchangeSpread:
    def __init__(self):
        self.highest_prices = {}
        self.lowest_prices = {}

    def update_spreads(self, price_data: PriceDataType):
        """
        Update the highest and lowest prices for each currency across all exchanges.
        Args:
            price_data: Dictionary containing price data.
        """
        for crypto, exchanges in price_data.items():
            if crypto not in self.highest_prices:
                self.highest_prices[crypto] = {}
            if crypto not in self.lowest_prices:
                self.lowest_prices[crypto] = {}

            for exchange, fiats in exchanges.items():
                for fiat, data in fiats.items():
                    price = data['price']

                    # Update highest prices
                    if fiat not in self.highest_prices[crypto] or price > self.highest_prices[crypto][fiat]['price']:
                        self.highest_prices[crypto][fiat] = {
                            'price': price,
                            'exchange': exchange,
                            'timestamp': data['timestamp']
                        }

                    # Update lowest prices
                    if fiat not in self.lowest_prices[crypto] or price < self.lowest_prices[crypto][fiat]['price']:
                        self.lowest_prices[crypto][fiat] = {
                            'price': price,
                            'exchange': exchange,
                            'timestamp': data['timestamp']
                        }

    def get_highest_prices(self):
        return self.highest_prices

    def get_lowest_prices(self):
        return self.lowest_prices
    
    def display_highest_prices(self):
        print("\n=== HIGHEST PRICES ===")
        for crypto, prices in self.highest_prices.items():
            for fiat, data in prices.items():
                print(f"{crypto} ({fiat}): {data['price']} on {data['exchange']} at {data['timestamp']}")
    
    def display_lowest_prices(self):
        print("\n=== LOWEST PRICES ===")
        for crypto, prices in self.lowest_prices.items():
            for fiat, data in prices.items():
                print(f"{crypto} ({fiat}): {data['price']} on {data['exchange']} at {data['timestamp']}")
    
    def display_spread(self):
        """Display the spread between highest and lowest prices for each crypto and fiat pair"""
        for crypto in self.highest_prices:
            for fiat in self.highest_prices[crypto]:
                highest_price = self.highest_prices[crypto][fiat]['price']
                lowest_price = self.lowest_prices[crypto][fiat]['price']
                spread = highest_price - lowest_price
                spread_percentage = (spread / lowest_price) * 100
                print(f"{crypto}/{fiat}: Spread: {spread:.2f} {fiat} ({spread_percentage:.2f}%)")
                print(f"  High: {highest_price:.2f} on {self.highest_prices[crypto][fiat]['exchange']}")
                print(f"  Low:  {lowest_price:.2f} on {self.lowest_prices[crypto][fiat]['exchange']}")
    
    def display_spreads(self):
        self.display_highest_prices()
        self.display_lowest_prices()    
    
# Example usage
if __name__ == "__main__":
    price_data = {
        'BTC': {
            'COINBASE': {
                'USD': {'price': 50000, 'timestamp': '2023-10-01T12:00:00'},
                'EUR': {'price': 45000, 'timestamp': '2023-10-01T12:01:00'}
            },
            'BINANCE': {
                'USD': {'price': 50500, 'timestamp': '2023-10-01T12:02:00'},
                'EUR': {'price': 45500, 'timestamp': '2023-10-01T12:03:00'}
            }
        },
        'ETH': {
            'COINBASE': {
                'USD': {'price': 3000, 'timestamp': '2023-10-01T12:00:00'},
                'EUR': {'price': 2700, 'timestamp': '2023-10-01T12:01:00'}
            },
            'BINANCE': {
                'USD': {'price': 3050, 'timestamp': '2023-10-01T12:02:00'},
                'EUR': {'price': 2750, 'timestamp': '2023-10-01T12:03:00'}
            }
        }
    }

    spread_tracker = ExchangeSpread()
    spread_tracker.update_spreads(price_data)
    print("Highest Prices:", spread_tracker.get_highest_prices())
    print("Lowest Prices:", spread_tracker.get_lowest_prices())
    spread_tracker.display_spread()
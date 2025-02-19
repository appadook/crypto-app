'''
This module is designed to collect data from the backend before being sent to
the frontend to be displayed in the UI. We use cross exchange arbitrage to get data
on the arbitrage across all exchanges and fiat currencies for cryptocurrencies.
We also use the fee calculator to get the fees for buying and selling cryptocurrencies
on different exchanges.
'''

import sys
import os
from typing import List, Dict, Any

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
    
    def get_arbitrage_data(self) -> Dict[str, Any]:
        """Get the arbitrage data from the cross exchange arbitrage class"""
        try:
            # Validate that we have sufficient data
            if not self.price_data or not self.exchange_rates:
                return {
                    'status': 'waiting',
                    'message': 'Waiting for price data and exchange rates...',
                    'opportunities': []
                }

            arbitrage_opportunities = self.cross_exchange_arbitrage.find_lowest_and_highest_price()
            if not arbitrage_opportunities:
                return {
                    'status': 'no_arbitrage',
                    'message': 'No arbitrage opportunities found',
                    'opportunities': []
                }

            # Process each opportunity with fees
            processed_opportunities = []
            for opp in arbitrage_opportunities:
                lowest_price = opp['lowest_price']
                lowest_price_exchange = opp['lowest_price_exchange'][1].lower()
                highest_price = opp['highest_price']
                highest_price_exchange = opp['highest_price_exchange'][1].lower()
                crypto = opp['crypto']
                buy_currency = opp['lowest_price_exchange'][2]
                sell_currency = opp['highest_price_exchange'][2]

                # Initialize fee calculator with correct parameters
                fee_calculator = FeeCalculator(
                    exchange_buy=lowest_price_exchange,
                    exchange_sell=highest_price_exchange,
                    crypto=crypto,
                    crypto_amount=1,
                    crypto_price_buy=lowest_price,
                    crypto_price_sell=highest_price,
                    currency_withdrawal=sell_currency,
                    exchange_rates=self.exchange_rates
                )

                # Calculate fees
                fees = fee_calculator.calculate_fees()
                
                processed_opportunities.append({
                    'crypto': crypto,
                    'lowest_price': round(lowest_price, 2),
                    'lowest_price_exchange': lowest_price_exchange,
                    'highest_price': round(highest_price, 2),
                    'highest_price_exchange': highest_price_exchange,
                    'buy_currency': buy_currency,
                    'sell_currency': sell_currency,
                    'spread_percentage': round(opp['spread'] * 100, 2),
                    'total_fees': round(fees['total_fees'], 2),
                    'arbitrage_after_fees': round(fees['arbitrage_after_fees'], 2),
                    'profit_percentage': round((fees['arbitrage_after_fees'] / lowest_price) * 100, 2)
                })

            return {    
                'status': 'success',
                'opportunities': processed_opportunities
            }
        except Exception as e:
            print(f"Error in get_arbitrage_data: {str(e)}")
            return {
                'status': 'error',
                'message': f'Error calculating arbitrage: {str(e)}',
                'opportunities': []
            }
    
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
        'USD': {'rate': 1.0, 'timestamp': '2023-10-01T00:00:00Z'},
        'EUR': {'rate': 1.1, 'timestamp': '2023-10-01T00:00:00Z'},  # 1 EUR = 1.1 USD
        'GBP': {'rate': 1.3, 'timestamp': '2023-10-01T00:00:00Z'}   # 1 GBP = 1.3 USD
    }
    data_collector = DataCollector(price_data, exchange_rates)
    arbitrage_data = data_collector.get_arbitrage_data()
    print(arbitrage_data)



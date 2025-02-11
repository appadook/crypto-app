import sys
import os

# from fee_calc import FeeCalc
from app.external.utilities.fee_calc import FeeCalculator
# Add the root directory of your project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import csv
from datetime import datetime
from app.types.price_data_types import PriceData
from app.external.utilities.cross_exchange_fiat_arbitrage import CrossExchangeFiatArbitrage


class CSVTracker:
    def __init__(self):
        self.fieldnames = ['exchange', 'currency', 'cryptocurrency', 'timestamp', 'price']
        self.file_path = self.create_csv()

    def get_arbitrage_strategy(self):
        """
        Get the arbitrage strategy based on the data from the cross exchnage arbitrage class
        Returns: 
            dict: Arbitrage data
            keys: lowest_price, lowest_price_exchange, highest_price, highest_price_exchange
        """
        cross_exchange_arbitrage = CrossExchangeFiatArbitrage(self.price_data, self.exchange_rates)
        arbitrage_data = cross_exchange_arbitrage.calculate_arbitrage()
        return arbitrage_data
    
    def store_data(self):
        arbitrage_data = self.get_arbitrage_strategy()
        lowest_price = arbitrage_data['lowest_price']
        lowest_price_exchange = arbitrage_data['lowest_price_exchange']
        highest_price = arbitrage_data['highest_price']
        highest_price_exchange = arbitrage_data['highest_price_exchange']
        timestamp = datetime.now().isoformat()
        strategy = f"Buy {lowest_price_exchange[0]} on {lowest_price_exchange[1]} in {lowest_price_exchange[2]} and sell on {highest_price_exchange[1]} in {highest_price_exchange[2]}"
        fees = None
        pass

    def store_price_data(self, price_data: PriceData):
        """
        Store the price data from nested dictionary structure into CSV file
        """
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            
            # Iterate through the nested structure
            for crypto in price_data:
                for exchange in price_data[crypto]:
                    for currency in price_data[crypto][exchange]:
                        data = price_data[crypto][exchange][currency]
                        
                        # Create a row dictionary matching the fieldnames
                        row = {
                            'exchange': exchange,
                            'currency': currency,
                            'cryptocurrency': crypto,
                            'timestamp': data['timestamp'],
                            'price': data['price']
                        }
                        
                        writer.writerow(row)

    
    def create_csv(self):
        '''
        Create a CSV file with today's date at name within this directory and returns the path to that csv file
        '''

        # Generate the filename with today's date
        today_date = datetime.now().strftime('%Y-%m-%d')
        new_file_path = os.path.join(os.path.dirname(__file__), f'data_{today_date}.csv')

        # Create the CSV file and write the header
        with open(new_file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()

        return new_file_path

if __name__ == '__main__':
    # Example usage
    price_data = {
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
            }
        }
    }

    csv_tracker = CSVTracker()
    csv_tracker.store_price_data(price_data)

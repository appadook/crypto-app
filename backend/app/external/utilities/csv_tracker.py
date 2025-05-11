import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from app.external.utilities.fee_calc import FeeCalculator
from app.external.utilities.exchange_spread import ExchangeSpread
from app.external.utilities.exchange_arbitrage import ExchangeArbitrage
from app.external.utilities.cross_exchange_fiat_arbitrage import CrossExchangeFiatArbitrage


import csv
from datetime import datetime
from app.types.price_data_types import PriceData
from app.external.utilities.cross_exchange_fiat_arbitrage import CrossExchangeFiatArbitrage


class CSVTracker:
    

    def write_spread_strategy(self, price_data):
        """
        Write spread strategy data to CSV file. The first table to represent the arbitrage with the same crypto
        and same fiat but across all exchanges.
        Args:
            price_data: Dictionary containing price data across exchanges
        """
        spread_tracker = ExchangeSpread()
        # Update the spread tracker with current prices
        spread_tracker.update_spreads(price_data)
        highest_prices = spread_tracker.get_highest_prices()
        lowest_prices = spread_tracker.get_lowest_prices()
        
        timestamp = datetime.now().isoformat()

        exchange_columns = [
            'BINANCE',
            'COINBASE',
            'KRAKEN', 
        ]
        fieldnames = ['trading_pair', 'timestamp'] + \
                         [f"{exchange}_price" for exchange in exchange_columns] + \
                         ['strategy', 'arbitrage_percentage']
        
        file_path = self.create_csv(fieldnames=fieldnames, name="crypto_fiat_arbitrage_1")

        # Check if file exists and is empty
        file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0
        
        # Open file in append mode
        with open(file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write header only if file is new or empty
            if not file_exists:
                writer.writeheader()
            
            # For each cryptocurrency and fiat pair
            for crypto in highest_prices:
                for fiat in highest_prices[crypto]:
                    # Count how many exchanges have data for this crypto/fiat pair
                    available_exchanges = sum(1 for exchange in exchange_columns 
                                           if exchange in price_data.get(crypto, {}) 
                                           and fiat in price_data[crypto][exchange])
                    
                    # Only proceed if at least 2 exchanges have data
                    if available_exchanges >= 2:
                        highest = highest_prices[crypto][fiat]
                        lowest = lowest_prices[crypto][fiat]
                        
                        # Calculate arbitrage percentage
                        arbitrage_percentage = ((highest['price'] - lowest['price']) / lowest['price']) * 100
                        
                        # Create strategy description
                        strategy = f"Buy at {lowest['exchange']} ({lowest['price']:.2f}) -> Sell at {highest['exchange']} ({highest['price']:.2f})"
                        
                        # Create base row data
                        row = {
                            'trading_pair': f"{crypto}/{fiat}",
                            'timestamp': timestamp,
                            'strategy': strategy,
                            'arbitrage_percentage': f"{arbitrage_percentage:.2f}%"
                        }
                        
                        # Add price for each exchange (including those not in current data)
                        for exchange in exchange_columns:
                            if exchange in price_data.get(crypto, {}) and fiat in price_data[crypto][exchange]:
                                row[f"{exchange}_price"] = f"{price_data[crypto][exchange][fiat]['price']:.2f}"
                            else:
                                row[f"{exchange}_price"] = "N/A"
                        
                        writer.writerow(row)

    def write_fiat_arbitrage(self, price_data, exchange_rates):
        """
        Write arbitrage opportunities between different fiat currencies for the same crypto on the same exchange.
        
        Args:
            price_data: Dictionary containing price data across exchanges and fiat pairs
        """
        timestamp = datetime.now().isoformat()
        supported_fiats = ['EUR', 'USD', 'GBP']
        fieldnames = ['crypto_exchange_pair', 'timestamp'] + \
                        supported_fiats + \
                        ['strategy', 'arbitrage_percentage']

        file_path = self.create_csv(fieldnames=fieldnames, name="crypto_exchange_arbitrage_2")

        # Check if file exists and is empty 
        file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0

        # Open file in append mode
        with open(file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write header if file is new/empty
            if not file_exists:
                writer.writeheader()

            # For each crypto and exchange pair
            for crypto, exchanges in price_data.items():
                for exchange, fiats in exchanges.items():
                    # Only process if there are at least 2 fiat prices for comparison
                    if len(fiats) >= 2:
                        # Initialize row with base data
                        row = {
                            'crypto_exchange_pair': f"{crypto}/{exchange}",
                            'timestamp': timestamp
                        }
                        
                        # Initialize fiat values
                        for fiat in supported_fiats:
                            if fiat in fiats:
                                row[fiat] = f"{fiats[fiat]['price']:.2f}"
                            else:
                                row[fiat] = "N/A"

                        # Use ExchangeArbitrage to calculate strategy and arbitrage
                        single_exchange_data = {crypto: {exchange: fiats}}
                        
                        arbitrage_calc = ExchangeArbitrage(single_exchange_data, exchange_rates)
                        arb_result = arbitrage_calc.find_lowest_and_highest_price()
                        
                        # Calculate arbitrage percentage
                        arbitrage_percentage = ((arb_result['highest_price'] - arb_result['lowest_price']) / 
                                             arb_result['lowest_price']) * 100
                        
                        # Create strategy description
                        strategy = (f"Buy in {arb_result['lowest_price_exchange'][2]} "
                                  f"({row[arb_result['lowest_price_exchange'][2]]}) -> "
                                  f"Sell in {arb_result['highest_price_exchange'][2]} "
                                  f"({row[arb_result['highest_price_exchange'][2]]})")
                        
                        row['strategy'] = strategy
                        row['arbitrage_percentage'] = f"{arbitrage_percentage:.2f}%"

                        writer.writerow(row)

    def write_cross_exchange_fiat_arbitrage(self, price_data, exchange_rates):
        """
        Write cross-exchange fiat arbitrage data to CSV, tracking arbitrage opportunities
        across different exchanges and fiat currencies for each crypto
        """
        # Define fieldnames based on README structure
        fieldnames = ['crypto', 'timestamp']
        
        # Add exchange/fiat pair columns
        supported_exchanges = ['COINBASE', 'BINANCE', 'KRAKEN', 'BITSTAMP']
        supported_fiats = ['USD', 'EUR', 'GBP']
        for exchange in supported_exchanges:
            for fiat in supported_fiats:
                fieldnames.append(f"{exchange}_{fiat}")
        fieldnames.extend(['strategy', 'arbitrage', 'total_fees', 'arbitrage_after_fees'])

        # Generate filename with today's date
        file_path = self.create_csv(fieldnames=fieldnames, name="crypto_arbitrage_3")

        # Check if file exists and is empty
        file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0

        # Open file in append mode
        with open(file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write header if file is new/empty
            if not file_exists:
                writer.writeheader()

            # For each cryptocurrency
            for crypto, exchanges in price_data.items():
                # Count exchanges that have any price data
                exchanges_with_data = set()
                total_price_points = 0
                
                # Count both total exchanges and total price points
                for exchange in exchanges:
                    if any(fiat in exchanges[exchange] for fiat in supported_fiats):
                        exchanges_with_data.add(exchange)
                        total_price_points += sum(1 for fiat in supported_fiats if fiat in exchanges[exchange])
                
                # Only proceed if we have at least 2 exchanges with data and at least 2 price points
                if len(exchanges_with_data) >= 2 and total_price_points >= 2:
                    # Initialize row with base data
                    row = {
                        'crypto': crypto,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }

                    # Fill in prices for each exchange/fiat pair
                    for exchange in supported_exchanges:
                        for fiat in supported_fiats:
                            column_name = f"{exchange}_{fiat}"
                            if exchange in exchanges and fiat in exchanges[exchange]:
                                row[column_name] = f"{exchanges[exchange][fiat]['price']:.2f}"
                            else:
                                row[column_name] = "N/A"

                    # Calculate arbitrage using CrossExchangeFiatArbitrage
                    arbitrage_calc = CrossExchangeFiatArbitrage(price_data, exchange_rates)
                    opportunities = arbitrage_calc.find_lowest_and_highest_price()
                    
                    # Filter opportunities for current crypto
                    crypto_opportunities = [opp for opp in opportunities if opp['crypto'] == crypto]
                    
                    # Process if we found opportunities for this crypto
                    if crypto_opportunities:
                        # Use the best opportunity (first in list since they're sorted by spread)
                        arb_result = crypto_opportunities[0]
                        
                        # Extract lowest and highest price info
                        lowest_price = arb_result['lowest_price']
                        highest_price = arb_result['highest_price']
                        lowest_exchange = arb_result['lowest_price_exchange']
                        highest_exchange = arb_result['highest_price_exchange']
                        
                        # Calculate arbitrage percentage
                        arbitrage_percentage = ((highest_price - lowest_price) / lowest_price) * 100

                        # Create strategy description
                        strategy = (f"Buy at {lowest_exchange[1]} in "
                                  f"{lowest_exchange[2]} -> Sell at "
                                  f"{highest_exchange[1]} in "
                                  f"{highest_exchange[2]}")

                        row['strategy'] = strategy
                        row['arbitrage'] = f"{arbitrage_percentage:.2f}%"

                        # Calculate fees using FeeCalculator
                        fee_calc = FeeCalculator(
                            exchange_buy=lowest_exchange[1],
                            exchange_sell=highest_exchange[1],
                            crypto=crypto,
                            crypto_amount=1,
                            crypto_price_buy=lowest_price,
                            crypto_price_sell=highest_price,
                            currency_withdrawal=highest_exchange[2],
                            exchange_rates=exchange_rates
                        )
                        
                        try:
                            fees = fee_calc.calculate_fees()
                            row['total_fees'] = f"${fees['total_fees']:.2f}"
                            row['arbitrage_after_fees'] = f"${fees['arbitrage_after_fees']:.2f}"
                            writer.writerow(row)
                        except Exception as e:
                            # print(f"DEBUG: Error calculating fees or writing row: {str(e)}")
                            continue

    def get_arbitrage_strategy(self):
        """
        Get the arbitrage strategy based on the data from the cross exchnage arbitrage class
        Returns: 
            dict: Arbitrage data
            keys: lowest_price, lowest_price_exchange, highest_price, highest_price_exchange
        """
        cross_exchange_arbitrage = CrossExchangeFiatArbitrage(self.price_data, self.exchange_rates)
        arbitrage_data = cross_exchange_arbitrage.find_lowest_and_highest_price()
        return arbitrage_data
    
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

    
    def create_csv(self, fieldnames, name):
        '''
        Create a CSV file with today's date and given name within this directory and returns the path to that csv file.
        Only creates the file if it doesn't already exist.
        '''

        # Generate the filename with today's date
        today_date = datetime.now().strftime('%Y-%m-%d')
        new_file_path = os.path.join(os.path.dirname(__file__), f'{name}_{today_date}.csv')

        # Only create file and write header if it doesn't exist
        if not os.path.exists(new_file_path):
            with open(new_file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

        return new_file_path

if __name__ == '__main__':
    # Example usage
    price_data = {
        'BTC': {
            'COINBASE': {
                'USD': {'price': 50000.0, 'timestamp': '2023-10-01T00:00:00Z'},
                # 'EUR': {'price': 45000.0, 'timestamp': '2023-10-01T00:00:00Z'},
                # 'GBP': {'price': 40000.0, 'timestamp': '2023-10-01T00:00:00Z'}
            },
            'BINANCE': {
                'USD': {'price': 50500.0, 'timestamp': '2023-10-01T00:00:00Z'},
                # 'EUR': {'price': 45500.0, 'timestamp': '2023-10-01T00:00:00Z'},
                # 'GBP': {'price': 40500.0, 'timestamp': '2023-10-01T00:00:00Z'}
            }
        }
    }
    exchange_rates = {
        'EUR': 1.0492,
        'GBP': 1.2587,
        'USD': 1.0000
    }

    csv_tracker = CSVTracker()
    csv_tracker.write_fiat_arbitrage(price_data, exchange_rates)
    csv_tracker.write_spread_strategy(price_data=price_data)
    csv_tracker.write_cross_exchange_fiat_arbitrage(price_data, exchange_rates)

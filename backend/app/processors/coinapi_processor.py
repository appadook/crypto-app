# backend/app/processors/coinapi_processor.py
import logging
from .base_processor import DataProcessor  # Import the DataProcessor base class

class CoinAPIProcessor(DataProcessor):  # Inherit from DataProcessor
    def __init__(self, price_tracker):
        self.logger = logging.getLogger(__name__)
        self.price_tracker = price_tracker  # Store the instance of PriceTracker

    def process_message(self, data):
        try:
            if data.get('type') == 'error':
                self.logger.error(f"CoinAPI error: {data}")
                return {'error': data}

            if 'price' not in data:
                return None

            symbol = data['symbol_id']
            price = data['price']
            exchange = symbol.split('_')[0]
            timestamp = data['time_exchange']

            if not (symbol.endswith('_USD') or symbol.endswith('_USDT')):
                return None

            if 'BINANCE' in exchange:
                exchange = 'BINANCE'

            crypto = None
            if 'BTC' in symbol:
                crypto = 'BTC'
            elif 'ETH' in symbol:
                crypto = 'ETH'

            if crypto and (symbol.endswith('_USD') or symbol.endswith('_USDT')):
                self.price_tracker.update_price(crypto, exchange, price, timestamp)  # Update price
                return {'prices': self.price_tracker.get_latest_prices()}  # Return latest prices

        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return None

    def get_latest_data(self) -> dict:
        """Retrieve the latest processed data as a dictionary."""
        return self.price_tracker.get_latest_prices()  # Return latest prices
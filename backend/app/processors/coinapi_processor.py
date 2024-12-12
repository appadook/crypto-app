# app/processors/coinapi_processor.py

from app.external.price_tracker import price_tracker
import logging
from .base_processor import DataProcessor  # Import the DataProcessor base class

logger = logging.getLogger(__name__)

class CoinAPIProcessor(DataProcessor):  # Inherit from DataProcessor
    def __init__(self):
        self.prices = {
            'BTC': {},
            'ETH': {}
        }

    def process_message(self, data):
        try:
            if data.get('type') == 'error':
                logger.error(f"CoinAPI error: {data}")
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
                price_tracker.update_price(crypto, exchange, price, timestamp)
                return {'prices': price_tracker.get_latest_prices()}

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {'error': str(e)}

        return None

    def get_latest_data(self) -> dict:
        """Retrieve the latest processed data as a dictionary."""
        return price_tracker.get_latest_prices()  # Example implementation
# backend/app/processors/coinapi_processor.py
import logging
from .base_processor import DataProcessor  # Import the DataProcessor base class

class CoinAPIProcessor(DataProcessor):  # Inherit from DataProcessor
    def __init__(self, price_tracker):
        self.logger = logging.getLogger(__name__)
        self.price_tracker = price_tracker  # Store the instance of PriceTracker

    def parse_crypto(self, symbol: str) -> str:
        supported_cryptos = ['BTC', 'ETH']
        for crypto in supported_cryptos:
            if crypto in symbol:
                return crypto
        return None

    def parse_exchange(self, symbol: str) -> str:
        exchange = symbol.split('_')[0]
        return 'BINANCE' if 'BINANCE' in exchange else exchange

    def parse_fiat(self, symbol: str) -> str:
        # print(f"Symbol: {symbol}")
        if symbol.endswith('_USD') or symbol.endswith('_USDT'):
            return 'USD'
        elif symbol.endswith('_EUR'):
            return 'EUR'
        print(f"Unsupported fiat currency for symbol: {symbol}")
        return None

    def parse_price(self, data: dict) -> float:
        return data.get('price')

    def parse_timestamp(self, data: dict) -> str:
        return data.get('time_exchange')

    def parse_message(self, data: dict) -> dict:
        if not data or 'price' not in data:
            return None

        symbol = data.get('symbol_id')
        if not symbol:
            return None

        return {
            'crypto': self.parse_crypto(symbol),
            'exchange': self.parse_exchange(symbol),
            'fiat': self.parse_fiat(symbol),
            'price': self.parse_price(data),
            'timestamp': self.parse_timestamp(data)
        }

    def process_message(self, data: dict) -> dict:
        try:
            if data.get('type') == 'error':
                self.logger.error(f"CoinAPI error: {data}")
                return {'error': data}

            parsed_data = self.parse_message(data)
            if not parsed_data or not parsed_data['crypto'] or not parsed_data['fiat']:
                return None

            self.price_tracker.update_price(
            crypto=parsed_data['crypto'],
            exchange=parsed_data['exchange'],
            price=parsed_data['price'],
            timestamp=parsed_data['timestamp'],
            fiat=parsed_data['fiat']
        )

            return {'prices': self.price_tracker.get_latest_prices()}

        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            return {'error': str(e)}

    def get_latest_data(self) -> dict:
        """Retrieve the latest processed data as a dictionary."""
        return self.price_tracker.get_latest_prices()  # Return latest prices
# backend/app/utils/price_tracker.py
import logging
from datetime import datetime

class PriceTracker:
    def __init__(self):
        self.crypto_prices = {
            'BTC': {},  # Exchange -> price mapping for Bitcoin
            'ETH': {}   # Exchange -> price mapping for Ethereum
        }
        self.message_count = 0
        self.logger = logging.getLogger(__name__)

    def update_price(self, crypto, exchange, price, timestamp):
        """Update the price of the cryptocurrency."""
        if crypto in self.crypto_prices:
            self.crypto_prices[crypto][exchange] = price
            self.message_count += 1
            self.logger.info(f"Updated {crypto} price to {price} on {exchange} at {timestamp}.")
        else:
            self.logger.error(f"Unknown cryptocurrency: {crypto}")

    def process_trade_message(self, data):
        try:
            symbol = data['symbol_id']
            price = data['price']
            exchange = symbol.split('_')[0]
            
            # Process only USD and USDT pairs
            if not (symbol.endswith('_USD') or symbol.endswith('_USDT')):
                return None

            # Normalize exchange names
            if 'BINANCE' in exchange:
                exchange = 'BINANCE'

            # Update price data
            if 'BTC' in symbol:
                self.crypto_prices['BTC'][exchange] = price
                crypto_type = 'BTC'
            elif 'ETH' in symbol:
                self.crypto_prices['ETH'][exchange] = price
                crypto_type = 'ETH'
            else:
                return None

            self.message_count += 1
            
            return {
                'timestamp': datetime.now().isoformat(),
                'price': price,
                'exchange': exchange
            }
        except Exception as e:
            self.logger.error(f"Error processing trade message: {e}")
            return None

    def get_latest_prices(self):
        return self.crypto_prices
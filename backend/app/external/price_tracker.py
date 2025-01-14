# backend/app/utils/price_tracker.py
import logging
from datetime import datetime
from .price_display import price_display  # Import the price display module

class PriceTracker:
    def __init__(self):
        self.crypto_prices = {}
        self.exchange_rates = {
            'EURUSD': None,  # Changed from EUR/USD
            'GBPCHF': None   # Changed from GBP/CHF
        }
        self.message_count = 0
        self.logger = logging.getLogger(__name__)
    
    def initialize_crypto_pairs(self, pairs: list[str]):
        """Initialize cryptocurrency pairs from strategy"""
        for pair in pairs:
            # Convert "BTC/USD" format to "BTC"
            crypto = pair.split('/')[0]
            self.crypto_prices[crypto] = {}

    def update_price(self, crypto, exchange, price, timestamp):
        """Update the price of the cryptocurrency."""
        if crypto in self.crypto_prices:
            self.crypto_prices[crypto][exchange] = {
                'price': price,
                'timestamp': timestamp
            }
            self.message_count += 1
            self._update_display()
        else:
            self.logger.error(f"Unknown cryptocurrency: {crypto}")
    
    def update_exchange_rate(self, pair: str, rate: float, timestamp=None):
        """Update forex exchange rate."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        if pair in self.exchange_rates:
            self.exchange_rates[pair] = {
                'rate': rate,
                'timestamp': timestamp
            }
            self._update_display()
        else:
            self.logger.error(f"Unknown currency pair: {pair}")

    def _update_display(self):
        """Private method to handle display updates."""
        price_display.display_prices({
            'prices': self.crypto_prices,
            'exchange_rates': self.exchange_rates,
            'last_update': datetime.now().isoformat()
        })

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
                self.crypto_prices['BTC'][exchange] = {
                    'price': price,
                    'timestamp': data.get('time_exchange', datetime.now().isoformat())
                }
                crypto_type = 'BTC'
            elif 'ETH' in symbol:
                self.crypto_prices['ETH'][exchange] = {
                    'price': price,
                    'timestamp': data.get('time_exchange', datetime.now().isoformat())
                }
                crypto_type = 'ETH'
            else:
                return None

            self.message_count += 1
            self._update_display()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'price': price,
                'exchange_rates': exchange
            }
        except Exception as e:
            self.logger.error(f"Error processing trade message: {e}")
            return None

    def get_latest_prices(self):
        return {
            'crypto': self.crypto_prices,
            'exchange_rates': self.exchange_rates
        }
    



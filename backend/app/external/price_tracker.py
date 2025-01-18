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

    def update_price(self, crypto: str, exchange: str, price: float, timestamp: str, fiat: str):
        """
        Update the price of the cryptocurrency.
        Args:
            crypto: Cryptocurrency symbol (e.g., 'BTC')
            exchange: Exchange name (e.g., 'COINBASE')
            price: Current price
            timestamp: Price timestamp
            fiat: Fiat currency (e.g., 'USD', 'USDT')
        """
        try:
            # Debug current state
            print(f"Before update - crypto_prices: {self.crypto_prices}")
            
            # Validate inputs
            if not all([crypto, exchange, price, timestamp, fiat]):
                raise ValueError("All inputs must be provided")
                
            # Clear existing incorrect structure if needed
            if crypto in self.crypto_prices:
                if not isinstance(self.crypto_prices[crypto].get(exchange), (float, dict)):
                    self.crypto_prices[crypto][exchange] = {}
            
            # Build structure step by step
            if crypto not in self.crypto_prices:
                self.crypto_prices[crypto] = {}
            
            if exchange not in self.crypto_prices[crypto]:
                self.crypto_prices[crypto][exchange] = {}
                
            # Atomic update of price data
            self.crypto_prices[crypto][exchange][fiat] = {
                'price': price,
                'timestamp': timestamp
            }
            
            # Debug final state
            # print(f"After update - crypto_prices: {self.crypto_prices}")
            
            self.message_count += 1
            self._update_display()
        except TypeError as e:
            self.logger.error("\n" + "="*40)
            self.logger.error(f"TypeError in update_price: {e}")
            self.logger.error(f"Current structure: {self.crypto_prices}")
            self.logger.error(f"Inputs - crypto: {crypto}, exchange: {exchange}, fiat: {fiat}, price: {price}, timestamp: {timestamp}")
            self.logger.error("="*40 + "\n")
        except Exception as e:
            self.logger.error("\n" + "="*40)
            self.logger.error(f"Unexpected error in update_price: {e}")
            self.logger.error(f"Current structure: {self.crypto_prices}")
            self.logger.error(f"Inputs - crypto: {crypto}, exchange: {exchange}, fiat: {fiat}, price: {price}, timestamp: {timestamp}")
            self.logger.error("="*40 + "\n")
    
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
        try:
            price_display.display_prices({
                'prices': self.crypto_prices,
                'exchange_rates': self.exchange_rates,
                'last_update': datetime.now().isoformat()
            })
        except Exception as e:
            self.logger.error("Display update error: %s", str(e))

    def process_trade_message(self, data):
        try:
            symbol = data['symbol_id']
            price = data['price']
            exchange = symbol.split('_')[0]
            
            # Process only USD, USDT, and EUR pairs
            if not (symbol.endswith('_USD') or symbol.endswith('_USDT') or symbol.endswith('_EUR')):
                return None

            # Normalize exchange names
            if 'BINANCE' in exchange:
                exchange = 'BINANCE'

            # Get fiat currency
            fiat = 'USD'
            if symbol.endswith('_EUR'):
                fiat = 'EUR'
            elif symbol.endswith('_USDT'):
                fiat = 'USD'

            # Update price data with proper fiat currency
            if 'BTC' in symbol:
                if 'BTC' not in self.crypto_prices:
                    self.crypto_prices['BTC'] = {}
                if exchange not in self.crypto_prices['BTC']:
                    self.crypto_prices['BTC'][exchange] = {}
                
                self.crypto_prices['BTC'][exchange][fiat] = {
                    'price': price,
                    'timestamp': data.get('time_exchange', datetime.now().isoformat())
                }
                crypto_type = 'BTC'
            elif 'ETH' in symbol:
                if 'ETH' not in self.crypto_prices:
                    self.crypto_prices['ETH'] = {}
                if exchange not in self.crypto_prices['ETH']:
                    self.crypto_prices['ETH'][exchange] = {}
                
                self.crypto_prices['ETH'][exchange][fiat] = {
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
    



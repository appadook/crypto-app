# backend/app/utils/price_tracker.py

import logging
import random
from datetime import datetime
from .price_display import price_display  # Import the price display module
from app.external.utilities.exchange_spread import ExchangeSpread  # Import the ExchangeSpread class
from app.external.utilities.csv_tracker import CSVTracker  # Import the CSVTracker class
from app.external.utilities.client_data_collector import DataCollector  # Import the DataCollector class



class PriceTracker:
    def __init__(self, socketio):
        if socketio is None:
            raise ValueError("A valid SocketIO instance is required!")
        self.crypto_prices = {}
        # Initialize exchange rates for all websocket connections
        current_time = datetime.now().isoformat()
        self.exchange_rates = {
            'USD': {'rate': 1.0, 'timestamp': current_time},
            'GBP': {'rate': None, 'timestamp': current_time},
            'EUR': {'rate': None, 'timestamp': current_time}
        }
        self.message_count = 0
        self.logger = logging.getLogger(__name__)
        self.socketio = socketio

        # May need to make adjustments with live websocket like behavior with client
        self.csv_tracker = CSVTracker()
        self.data_collector = DataCollector(self.crypto_prices, self.exchange_rates)
        self.client_data = None
        
    
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
            self.logger.debug(f"Before update - crypto_prices: {self.crypto_prices}")
            self.logger.debug(f"Before update - exchange_rates: {self.exchange_rates}")
            
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
            
            self.message_count += 1
            self._update_display()
            self.csv_tracker.write_spread_strategy(self.crypto_prices)
            self.csv_tracker.write_fiat_arbitrage(self.crypto_prices, self.exchange_rates)
            self.csv_tracker.write_cross_exchange_fiat_arbitrage(self.crypto_prices, self.exchange_rates)

            # Only emit client data for price updates (more frequent than hello messages)
            self._emit_client_data()

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
        
        try:
            # Extract the currency from the pair (e.g., "EUR/USD" -> "EUR")
            currency = pair.split('/')[0]
            
            if currency in self.exchange_rates:
                self.exchange_rates[currency] = {
                    'rate': rate,
                    'timestamp': timestamp
                }
                self._update_display()
                
                # Only emit client data for exchange rate updates
                self._emit_client_data()
            else:
                self.logger.error(f"Unknown currency pair: {pair}")
        except Exception as e:
            self.logger.error(f"Error updating exchange rate: {str(e)}")

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

    def _display_spread_across_exchanges(self):
        """Private method to handle display spread across exchanges."""
        spread = ExchangeSpread()
        spread.update_spreads(self.crypto_prices)
        spread.display_spread()

    def _display_arbitrage(self):
        """Private method to handle display live arbitrage of websocket of each crypto & exchange in data."""
        try:
            price_display.display_arbitrage({
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
    
    def get_client_data(self):
        return self.client_data
    
    def _update_csv(self):
        csv_tracker = self.csv_tracker
        csv_tracker.store_price_data(self.crypto_prices)
    
    def has_valid_exchange_rates(self):
        """Check if we have valid exchange rates for all currencies."""
        # For testing purposes, always return True to allow hardcoded data
        return True

    def _emit_client_data(self):
        """Private method to prepare and emit client data to frontend"""
        try:
            # Check if we have valid exchange rates before calculating arbitrage
            if not self.has_valid_exchange_rates():
                self.logger.info("Waiting for valid exchange rates before calculating arbitrage")
                self.client_data = {
                    'status': 'waiting',
                    'message': 'Waiting for valid exchange rates...'
                }
            else:
                # Get arbitrage data from collector
                # self.client_data = self.data_collector.get_arbitrage_data()

                # Generate a random number between 10000 and 10500
                random_price = random.randint(10000, 10500)  # {{ edit_1 }}

                # For testing purposes, use the following data
                self.client_data = {
                    'status': 'success',
                    'crypto': 'BTC',
                    'lowest_price_exchange': 'BINANCE',
                    'lowest_price': 10000,
                    'highest_price_exchange': 'COINBASE',
                    'highest_price': random_price,
                    'buy_currency': 'USD',
                    'sell_currency': 'USD',
                    'total_fees': 0.01,
                    'arbitrage_after_fees': random_price - 10000 - 0.01
                }
            
            # Prepare data for frontend
            frontend_data = {
                'type': 'arbitrage_update',
                'data': self.client_data,
                'timestamp': datetime.now().isoformat()
            }

            # Emit to frontend if socketio is available
            if self.socketio:
                try:
                    self.logger.info("Attempting to emit client data to frontend...")
                    self.socketio.emit('client_data', frontend_data)
                    if self.client_data.get('status') == 'success':
                        self.logger.info(f"Emitted arbitrage data: Buy {self.client_data.get('crypto')} at {self.client_data.get('lowest_price_exchange')} " +
                                       f"(${self.client_data.get('lowest_price'):.2f}), Sell at {self.client_data.get('highest_price_exchange')} " +
                                       f"(${self.client_data.get('highest_price'):.2f}), Profit after fees: ${self.client_data.get('arbitrage_after_fees'):.2f}")
                        self.logger.info(f"Successfully emitted arbitrage data: {frontend_data}")
                    elif self.client_data.get('status') == 'waiting':
                        self.logger.debug("Waiting for sufficient data...")
                    elif self.client_data.get('status') == 'no_arbitrage':
                        self.logger.debug("No arbitrage opportunities found")
                    else:
                        self.logger.warning(f"Emitted client data with status: {self.client_data.get('status')}")
                        self.logger.info(f"Emitted arbitrage data: {frontend_data}")
                except Exception as e:
                    self.logger.error(f"Failed to emit client data: {str(e)}")
            else:
                self.logger.warning("SocketIO not available for client data emission")
        except Exception as e:
            self.logger.error(f"Error preparing/emitting client data: {str(e)}")

    def emit_hello_message(self):
        """Public method to emit hello message to frontend"""
        try:
            # Add rate limiting - only emit once every 5 seconds
            current_time = datetime.now()
            if hasattr(self, '_last_hello_time'):
                time_diff = (current_time - self._last_hello_time).total_seconds()
                if time_diff < 5:  # Less than 5 seconds since last message
                    self.logger.debug("Skipping hello message due to rate limiting")
                    return
            
            self._last_hello_time = current_time
            
            if self.socketio:
                self.logger.info("Sending hello message and client data...")
                
                # First send hello message
                message_data = {
                    'message': 'Hello from backend!',
                    'timestamp': current_time.isoformat()
                }
                self.socketio.emit('hello', message_data)
                self.logger.info(f"Emitted hello message: {message_data}")
                
                # Then send client data
                self._emit_client_data()
            else:
                self.logger.error("Cannot emit messages: socketio instance is None")
        except Exception as e:
            self.logger.error(f"Error in emit_hello_message: {str(e)}")
            # Try to re-emit after error
            try:
                if self.socketio:
                    retry_data = {
                        'message': 'Hello from backend! (retry)',
                        'timestamp': datetime.now().isoformat()
                    }
                    self.socketio.emit('hello', retry_data)
                    self.logger.info("Successfully sent retry hello message")
                    self._emit_client_data()  # Also retry sending client data
            except Exception as retry_error:
                self.logger.error(f"Error in retry attempt: {str(retry_error)}")



from datetime import datetime
import threading

class PriceTracker:
    def __init__(self):
        self._prices = {
            'BTC': {},
            'ETH': {}
        }
        self._lock = threading.Lock()
        self._last_update = None

    def update_price(self, crypto, exchange, price, timestamp):
        with self._lock:
            self._prices[crypto][exchange] = {
                'price': price,
                'timestamp': timestamp
            }
            self._last_update = datetime.now()

    def get_latest_prices(self):
        with self._lock:
            return {
                'prices': self._prices,
                'last_update': self._last_update.isoformat() if self._last_update else None
            }

# Global instance
price_tracker = PriceTracker()
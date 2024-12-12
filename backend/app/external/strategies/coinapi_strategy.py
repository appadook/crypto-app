import json
import logging
import os
from datetime import datetime
from .base_strategy import WebSocketStrategy
from app.config.settings import Config
from app.external.price_tracker import price_tracker

logger = logging.getLogger(__name__)

class CoinAPIStrategy(WebSocketStrategy):
    def __init__(self):
        self.api_key = Config.COINAPI_KEY
        self.prices = {
            'BTC': {},
            'ETH': {}
        }
        
    def get_connection_params(self):
        return {
            "uri": "wss://ws.coinapi.io/v1/"
        }

    def format_auth_message(self):
        return {
            "type": "hello",
            "apikey": self.api_key,
            "heartbeat": False,
            "subscribe_data_type": ["trade"],
            "subscribe_filter_symbol_id": [
                "BITSTAMP_SPOT_BTC_USD", "BITSTAMP_SPOT_ETH_USD",
                "KRAKEN_SPOT_BTC_USD", "KRAKEN_SPOT_ETH_USD",
                "BINANCE_SPOT_BTC_USDT", "BINANCE_SPOT_ETH_USDT",
                "COINBASE_SPOT_BTC_USD", "COINBASE_SPOT_ETH_USD"
            ]
        }

    async def process_message(self, message):
        try:
            data = json.loads(message)
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

    def get_supported_pairs(self) -> list[str]:
        return ["BTC/USD", "ETH/USD"]

    def get_name(self) -> str:
        return "coinapi"
# backend/app/external/strategies/coinapi_strategy.py
import json
import logging
from .base_strategy import WebSocketStrategy
from app.config.settings import Config
from app.processors.coinapi_processor import CoinAPIProcessor

logger = logging.getLogger(__name__)

class CoinAPIStrategy(WebSocketStrategy):
    def __init__(self, price_tracker):
        self.api_key = Config.COINAPI_KEY
        self.processor = CoinAPIProcessor(price_tracker)  # Instantiate the processor
        self.price_tracker = price_tracker  # Reference to the price tracker
        self.price_tracker.initialize_crypto_pairs(self.get_supported_pairs())

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
        data = json.loads(message)
        # Use only processor path for updates
        self.processor.process_message(data)

    def get_supported_pairs(self) -> list[str]:
        return ["BTC/USD", "ETH/USD"]

    def get_name(self) -> str:
        return "coinapi"
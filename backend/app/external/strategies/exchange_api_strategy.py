from .base_strategy import WebSocketStrategy
from app.config.settings import Config
from app.processors.xchange_processor import XChangeProcessor
import json
import logging

logger = logging.getLogger(__name__)

class ExchangeAPIStrategy(WebSocketStrategy):
    def __init__(self, price_tracker):
        self.api_key = Config.XCHANGEAPI_KEY
        self.price_tracker = price_tracker
        self.processor = XChangeProcessor()
        self.connected = False
        self.logger = logging.getLogger(__name__)

    def get_connection_params(self):
        self.logger.info("Initializing xChangeAPI connection...")
        return {
            "uri": f"wss://api.xchangeapi.com/websocket/live?api-key={self.api_key}"
        }

    def format_auth_message(self):
        pairs = self.get_supported_pairs()
        self.logger.info(f"Subscribing to pairs: {pairs}")
        return {"pairs": pairs}

    async def process_message(self, message):
        try:
            self.logger.debug(f"Processing message: {message[:50]}...")
            
            # Handle initial connection
            if not self.connected and message.startswith('0'):
                self.connected = True
                self.logger.info("Successfully connected to xChangeAPI!")
                return self.processor.process_message(message)

            # Handle heartbeat
            if message.startswith('2'):
                self.logger.debug("Received heartbeat")
                return "heartbeat"

            # Process regular messages
            result = self.processor.process_message(message)
            if isinstance(result, dict) and 'name' in result and 'ask' in result:
                # The name is already normalized by the processor
                pair = result["name"]  # No need to normalize again
                self.logger.info(f"Updating rate for {pair}: {result['ask']}")
                self.price_tracker.update_exchange_rate(
                    pair,
                    float(result["ask"]),
                    result.get("timestamp")
                )
            
            return result

        except Exception as e:
            self.logger.error(f"Message processing error: {e}")
            return None

    def get_supported_pairs(self) -> list[str]:
        return ["EURUSD", "GBPUSD"]

    def get_name(self) -> str:
        return "xchangeapi"
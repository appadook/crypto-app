import websockets
import asyncio
import logging
import json
from app.external.strategies.coinapi_strategy import CoinAPIStrategy
from app.external.price_tracker import PriceTracker
from app.external.strategies.exchange_api_strategy import ExchangeAPIStrategy
# Add more strategy imports as needed

logger = logging.getLogger(__name__)
price_tracker = PriceTracker()

class WebSocketClient:
    def __init__(self):
        self.strategies = {
            'coinapi': CoinAPIStrategy(price_tracker),
            'xchangeapi': ExchangeAPIStrategy(price_tracker)
            # Add more strategies here
        }
        self.running = False
        self.broadcast_callback = None

    async def connect_with_strategy(self, strategy_name):
        strategy = self.strategies.get(strategy_name)
        if not strategy:
            logger.error(f"Unknown strategy: {strategy_name}")
            return

        params = strategy.get_connection_params()
        try:
            async with websockets.connect(params['uri']) as websocket:
                auth_message = strategy.format_auth_message()
                await websocket.send(json.dumps(auth_message))

                while self.running:
                    message = await websocket.recv()
                    processed_data = await strategy.process_message(message)
                    if processed_data:
                        # Broadcast to websocket clients
                        if self.broadcast_callback:
                            self.broadcast_callback(f'{strategy_name}_update', processed_data)

        except Exception as e:
            logger.error(f"WebSocket error for {strategy_name}: {e}")

    def start(self, broadcast_fn):
        self.running = True
        self.broadcast_callback = broadcast_fn
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        tasks = [
            self.connect_with_strategy(strategy_name)
            for strategy_name in self.strategies.keys()
        ]
        loop.run_until_complete(asyncio.gather(*tasks))

    def stop(self):
        self.running = False

# Global instance
ws_client = WebSocketClient()
start_external_websockets = ws_client.start
stop_external_websockets = ws_client.stop
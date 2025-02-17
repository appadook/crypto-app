import websockets
import asyncio
import logging
import json
import threading
from app.socketio_instance import socketio
from app.external.strategies.coinapi_strategy import CoinAPIStrategy
from app.price_tracker_instance import price_tracker
from app.external.strategies.exchange_api_strategy import ExchangeAPIStrategy
# Add more strategy imports as needed

logger = logging.getLogger(__name__)

class WebSocketClient:
    def __init__(self):
        self.strategies = {
            'coinapi': CoinAPIStrategy(price_tracker),
            'xchangeapi': ExchangeAPIStrategy(price_tracker)
            # Add more strategies here
        }
        self.running = False
        self.broadcast_callback = None
        self.thread = None
        self.loop = None

    async def connect_with_strategy(self, strategy_name):
        strategy = self.strategies.get(strategy_name)
        if not strategy:
            logger.error(f"Unknown strategy: {strategy_name}")
            return

        params = strategy.get_connection_params()
        while self.running:  # Keep trying to reconnect while running
            try:
                async with websockets.connect(params['uri']) as websocket:
                    auth_message = strategy.format_auth_message()
                    await websocket.send(json.dumps(auth_message))
                    logger.info(f"Successfully connected to {strategy_name}")

                    while self.running:
                        try:
                            message = await websocket.recv()
                            processed_data = await strategy.process_message(message)
                            if processed_data and self.broadcast_callback:
                                self.broadcast_callback(f'{strategy_name}_update', processed_data)
                        except websockets.exceptions.ConnectionClosed:
                            logger.warning(f"Connection closed for {strategy_name}, attempting to reconnect...")
                            break
                        except Exception as e:
                            logger.error(f"Error processing message for {strategy_name}: {e}")
                            continue

            except Exception as e:
                logger.error(f"WebSocket connection error for {strategy_name}: {e}")
                if self.running:
                    logger.info(f"Retrying connection for {strategy_name} in 5 seconds...")
                    await asyncio.sleep(5)  # Wait before retrying

    def run_websocket_loop(self):
        """Run the websocket event loop in a separate thread"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        tasks = [
            self.connect_with_strategy(strategy_name)
            for strategy_name in self.strategies.keys()
        ]
        
        try:
            self.loop.run_until_complete(asyncio.gather(*tasks))
        except Exception as e:
            logger.error(f"Error in websocket loop: {e}")
        finally:
            self.loop.close()

    def start(self, broadcast_fn):
        if self.running:
            logger.warning("WebSocket client is already running")
            return

        self.running = True
        self.broadcast_callback = broadcast_fn
        
        # Start websocket loop in a separate thread
        self.thread = threading.Thread(target=self.run_websocket_loop)
        self.thread.daemon = True  # Thread will exit when main program exits
        self.thread.start()
        
        logger.info("WebSocket client started in background thread")

    def stop(self):
        logger.info("Stopping WebSocket client...")
        self.running = False
        
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)  # Wait up to 5 seconds for clean shutdown
        
        logger.info("WebSocket client stopped")

# Global instance
ws_client = WebSocketClient()
start_external_websockets = ws_client.start
stop_external_websockets = ws_client.stop
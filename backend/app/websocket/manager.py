from flask import request
from flask_socketio import emit
import threading
import logging
from app.external import start_external_websockets, stop_external_websockets

class WebSocketManager:
    def __init__(self, socketio):
        self.socketio = socketio
        self.clients = {}  # Change to dict to store client subscriptions
        self.external_ws_thread = None
        self.logger = logging.getLogger(__name__)

    def handle_connect(self):
        try:
            self.clients[request.sid] = set()  # Initialize empty subscription set
            self.logger.info(f"Client connected: {request.sid}")
            self._ensure_external_websocket()
        except Exception as e:
            self.logger.error(f"Connection error: {str(e)}")
            raise

    def handle_disconnect(self):
        try:
            if request.sid in self.clients:
                del self.clients[request.sid]
                self.logger.info(f"Client disconnected: {request.sid}")
                if not self.clients:
                    self._stop_external_websocket()
        except Exception as e:
            self.logger.error(f"Disconnection error: {str(e)}")

    def add_subscription(self, client_id, sources):
        if client_id in self.clients:
            self.clients[client_id].update(sources)
            return True
        return False

    def _ensure_external_websocket(self):
        if not self.external_ws_thread or not self.external_ws_thread.is_alive():
            self.external_ws_thread = threading.Thread(
                target=start_external_websockets,
                args=(self.broadcast,),  # Pass broadcast method to external client
                daemon=True
            )
            self.external_ws_thread.start()

    def _stop_external_websocket(self):
        if self.external_ws_thread:
            stop_external_websockets()
            self.external_ws_thread = None

    def broadcast(self, event, data):
        try:
            self.socketio.emit(event, data)
        except Exception as e:
            self.logger.error(f"Broadcasting error: {str(e)}")
from flask import request
from flask_socketio import emit
import threading
import logging
from app.external.websocket_client import WebSocketClient, start_external_websockets, stop_external_websockets
from app.price_tracker_instance import price_tracker

class WebSocketManager:
    def __init__(self, socketio):
        self.socketio = socketio
        self.clients = {}  # Store client subscriptions
        self.external_client = WebSocketClient()  # External WebSocket client
        self.external_ws_thread = None
        self.logger = logging.getLogger(__name__)

    def handle_connect(self):
        """Handle new frontend client connection"""
        try:
            client_id = request.sid
            self.clients[client_id] = {
                'subscriptions': set(),
                'feeds': set(),
                'connected_at': threading.current_thread().name
            }
            self.logger.info(f"Client connected: {client_id}")
            self._ensure_external_connections()
            return True
        except Exception as e:
            self.logger.error(f"Connection error: {str(e)}")
            return False

    def handle_disconnect(self):
        """Handle frontend client disconnection"""
        try:
            client_id = request.sid
            if client_id in self.clients:
                del self.clients[client_id]
                self.logger.info(f"Client disconnected: {client_id}")
                if not self.clients:
                    self._stop_external_connections()
        except Exception as e:
            self.logger.error(f"Disconnection error: {str(e)}")

    def add_subscription(self, client_id, sources):
        """Add data source subscriptions for a client"""
        try:
            if client_id in self.clients:
                self.clients[client_id]['subscriptions'].update(sources)
                self._ensure_external_connections()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Subscription error: {str(e)}")
            return False

    def add_feed(self, client_id, feeds):
        """Add feed subscriptions for a client"""
        try:
            if client_id in self.clients:
                self.clients[client_id]['feeds'].update(feeds)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Feed subscription error: {str(e)}")
            return False

    def _ensure_external_connections(self):
        """Ensure external WebSocket connections are active"""
        if not self.external_ws_thread or not self.external_ws_thread.is_alive():
            self.external_ws_thread = threading.Thread(
                target=start_external_websockets,
                args=(self.broadcast_update,),
                daemon=True
            )
            self.external_ws_thread.start()
            self.logger.info("Started external WebSocket connections")

    def _stop_external_connections(self):
        """Stop external WebSocket connections"""
        if self.external_ws_thread:
            stop_external_websockets()
            self.external_ws_thread = None
            self.logger.info("Stopped external WebSocket connections")

    def broadcast_update(self, event, data):
        """Broadcast updates to relevant subscribed clients"""
        try:
            # Broadcast to all clients for now - you can implement filtering based on subscriptions
            self.socketio.emit(event, data)
            self.logger.debug(f"Broadcasted {event} to clients")
        except Exception as e:
            self.logger.error(f"Broadcasting error: {str(e)}")

    def get_client_info(self, client_id):
        """Get information about a specific client"""
        return self.clients.get(client_id)

    def get_active_clients(self):
        """Get list of all active clients"""
        return list(self.clients.keys())
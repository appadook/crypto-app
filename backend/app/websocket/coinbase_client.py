# app/websocket/coinbase_client.py
import websocket
import json
from flask_socketio import emit

class CoinbaseWebsocketClient:
    def __init__(self, socketio):
        self.ws = None
        self.socketio = socketio
        
    def connect(self):
        self.ws = websocket.WebSocketApp(
            "wss://ws-feed.pro.coinbase.com",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
    def subscribe(self, product_ids):
        subscribe_message = {
            "type": "subscribe",
            "product_ids": product_ids,
            "channels": ["ticker"]
        }
        self.ws.send(json.dumps(subscribe_message))
        
    def on_message(self, ws, message):
        data = json.loads(message)
        self.socketio.emit('price_update', data)
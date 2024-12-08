# app/routes/websocket_routes.py
from flask import Blueprint
from flask_socketio import emit
from ..websocket.coinbase_client import CoinbaseWebsocketClient
from ..services.arbitrage_service import ArbitrageService

bp = Blueprint('ws', __name__)
arbitrage_service = ArbitrageService()
ws_client = None

def init_websocket(socketio):
    global ws_client
    ws_client = CoinbaseWebsocketClient(socketio)
    
    @socketio.on('connect')
    def handle_connect():
        ws_client.connect()
        ws_client.subscribe(['BTC-USD', 'ETH-USD'])  # Add more pairs as needed
        
    @socketio.on('price_update')
    def handle_price_update(data):
        arbitrage_service.update_price(data['product_id'], data['price'])
        arbitrage_index = arbitrage_service.calculate_arbitrage_index()
        emit('arbitrage_update', arbitrage_index)
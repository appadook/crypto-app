# backend/app/routes/routes.py
from flask import Blueprint, jsonify
from app.external.price_tracker import PriceTracker
from datetime import datetime
from flask_socketio import emit

main_bp = Blueprint('main', __name__)
price_tracker = PriceTracker()  # Instantiate the PriceTracker

@main_bp.route('/api/latest-prices', methods=['GET'])
def get_latest_prices():
    latest_data = price_tracker.get_latest_prices()  # Fetch latest prices
    response = {
        "status": "success",
        "crypto_prices": latest_data['crypto'],
        "exchange_rates": latest_data['exchange_rates'],
        "timestamp": datetime.now().isoformat()
    }
    return jsonify(response)

@main_bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})


# WebSocket event to send data to the client
@main_bp.route('/socketio/connect')
def handle_connect():
    from app import socketio
    @socketio.on('connect')
    def connect():
        emit('client data', price_tracker.get_client_data())

@main_bp.route('/socketio/disconnect')
def handle_disconnect():
    from app import socketio
    @socketio.on('disconnect')
    def disconnect():
        print('Client disconnected')
from flask import Blueprint, jsonify
from app.price_tracker_instance import price_tracker
from datetime import datetime

test_bp = Blueprint('test', __name__)

@test_bp.route('/test/update-price', methods=['GET'])
def test_price_update():
    """Test endpoint to trigger a price update"""
    try:
        # Simulate a price update
        price_tracker.update_price(
            crypto='BTC',
            exchange='TESTEX',
            price=50000.0,
            timestamp=datetime.now().isoformat(),
            fiat='USD'
        )
        return jsonify({'status': 'success', 'message': 'Test price update sent'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@test_bp.route('/test/multiple-updates', methods=['GET'])
def test_multiple_updates():
    """Test endpoint to trigger multiple price updates"""
    try:
        # Simulate multiple price updates
        test_data = [
            ('BTC', 'BINANCE', 50000.0, 'USD'),
            ('ETH', 'BINANCE', 3000.0, 'USD'),
            ('BTC', 'COINBASE', 50100.0, 'USD'),
            ('ETH', 'COINBASE', 3010.0, 'USD'),
        ]
        
        timestamp = datetime.now().isoformat()
        for crypto, exchange, price, fiat in test_data:
            price_tracker.update_price(
                crypto=crypto,
                exchange=exchange,
                price=price,
                timestamp=timestamp,
                fiat=fiat
            )
        
        return jsonify({
            'status': 'success',
            'message': 'Multiple test updates sent',
            'updates': len(test_data)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500 
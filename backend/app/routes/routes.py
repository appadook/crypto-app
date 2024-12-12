
from flask import jsonify
from app.routes import main_bp
from app.external.price_tracker import price_tracker

@main_bp.route('/api/prices', methods=['GET'])
def get_prices():
    return jsonify(price_tracker.get_latest_prices())

@main_bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})
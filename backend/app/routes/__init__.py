
from flask import Blueprint

main_bp = Blueprint('main', __name__)

from app.routes import routes  # Import routes
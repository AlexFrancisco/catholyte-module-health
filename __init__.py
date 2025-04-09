from flask import Blueprint

health_tracker_bp = Blueprint('health_tracker', __name__, template_folder='templates')

from app.modules.health import routes  # Import routes to register them
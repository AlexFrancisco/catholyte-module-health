from flask import Blueprint, request

health_tracker_bp = Blueprint('health_tracker', __name__, template_folder='templates')

@health_tracker_bp.context_processor
def inject_template_vars():
    """Make breadcrumbs available in all health module templates."""
    # Define breadcrumb mappings based on routes
    breadcrumbs = {
        'health_tracker.dashboard': [('Health Dashboard', None)],
        'health_tracker.health': [('Health Dashboard', None)],
        'health_tracker.exercises': [('Health Dashboard', 'health_tracker.health'), ('Exercises', None)],
        'health_tracker.diet': [('Health Dashboard', 'health_tracker.health'), ('Diet', None)],
        'health_tracker.glucose': [('Health Dashboard', 'health_tracker.health'), ('Glucose', None)],
        'health_tracker.medications': [('Health Dashboard', 'health_tracker.health'), ('Medications', None)],
        'health_tracker.edit_medication': [('Health Dashboard', 'health_tracker.health'), ('Medications', 'health_tracker.medications'), ('Edit Medication', None)],
        'health_tracker.measurements': [('Health Dashboard', 'health_tracker.health'), ('Measurements', None)],
        'health_tracker.documents': [('Health Dashboard', 'health_tracker.health'), ('Documents', None)],
        'health_tracker.calendar': [('Health Dashboard', 'health_tracker.health'), ('Health Calendar', None)],
        # Add breadcrumbs for appointments
        'health_tracker.appointments': [('Health Dashboard', 'health_tracker.health'), ('Appointments', None)],
        'health_tracker.edit_appointment': [('Health Dashboard', 'health_tracker.health'), ('Appointments', 'health_tracker.appointments'), ('Edit Appointment', None)],
        'health_tracker.conditions': [('Health Dashboard', 'health_tracker.health'), ('Medical Conditions', None)],
        'health_tracker.edit_condition': [('Health Dashboard', 'health_tracker.health'), ('Medical Conditions', 'health_tracker.conditions'), ('Edit Condition', None)],
        'health_tracker.view_condition': [('Health Dashboard', 'health_tracker.health'), ('Medical Conditions', 'health_tracker.conditions'), ('View Condition', None)],
    }
    
    # Get current endpoint
    endpoint = request.endpoint
    
    # Return the relevant breadcrumbs for the current endpoint
    return {
        'breadcrumbs': breadcrumbs.get(endpoint, []),
        'now': datetime.now()  # Add current datetime for appointment comparisons
    }

from app.modules.health import routes
from datetime import datetime  # Add this import
from app import db
from datetime import datetime

class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # Type of health record (e.g., 'exercise', 'diet', 'glucose', 'medication', 'measurement')
    name = db.Column(db.String(128), nullable=True)  # Name of the exercise, meal, medication, etc.
    value = db.Column(db.Float, nullable=True)  # Numeric value (e.g., calories, glucose level, weight)
    duration = db.Column(db.Integer, nullable=True)  # Duration in minutes (for exercises)
    dose = db.Column(db.String(64), nullable=True)  # Dose (for medications)
    date = db.Column(db.String(64), nullable=False)  # Date of the record
    content = db.Column(db.Text, nullable=True)  # Additional HTML content (e.g., meal description, exercise details)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"HealthRecord('{self.type}', '{self.name}', '{self.value}', '{self.date}', '{self.content}')"

class HealthDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=True)  # Extracted/OCR text content
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, processed, failed

class Medication(db.Model):
    """Model for tracking detailed medication information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # Medication Name
    strength = db.Column(db.String(64), nullable=True)  # Strength (e.g., "20 mg tablet")
    dosage_schedule = db.Column(db.String(128), nullable=True)  # Dosage Schedule (e.g., "1 tablet twice daily")
    timing = db.Column(db.String(128), nullable=True)  # Timing (e.g., "Morning & Evening")
    food_relation = db.Column(db.String(128), nullable=True)  # With/After Food? (e.g., "Before meals (empty stomach)")
    description = db.Column(db.Text, nullable=True)  # Description of medication purpose
    pill_description = db.Column(db.Text, nullable=True)  # Physical description of the pill
    
    # Status tracking
    active = db.Column(db.Boolean, default=True)  # Whether medication is currently being taken
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Medication('{self.name}', '{self.strength}', active={self.active})"

class Appointment(db.Model):
    """Model for tracking medical and therapy appointments"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)  # Brief description of appointment
    appointment_type = db.Column(db.String(64), nullable=False)  # 'medical', 'therapy', 'dental', etc.
    provider_name = db.Column(db.String(128), nullable=True)  # Doctor/therapist name
    
    # Date and time
    date = db.Column(db.DateTime, nullable=False)
    
    # Basic details
    location = db.Column(db.String(255), nullable=True)
    virtual = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)  # Any preparation or follow-up notes
    
    # Status tracking
    status = db.Column(db.String(20), nullable=False, default='scheduled')  # scheduled, completed, canceled
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Appointment('{self.title}', '{self.appointment_type}', {self.date.strftime('%Y-%m-%d %H:%M')})"
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
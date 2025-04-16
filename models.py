from app import db
from datetime import datetime

class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # Type of health record
    name = db.Column(db.String(128), nullable=True)
    value = db.Column(db.Float, nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    dose = db.Column(db.String(64), nullable=True)
    date = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Images relationship
    images = db.relationship('HealthRecordImage', back_populates='record', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"HealthRecord('{self.type}', '{self.name}', '{self.date}')"
    
    @property
    def primary_image(self):
        """Return the primary image or first image if no primary set"""
        primary = next((img for img in self.images if img.is_primary), None)
        return primary or (self.images[0] if self.images else None)


class HealthRecordImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_primary = db.Column(db.Boolean, default=False)
    prompt = db.Column(db.String(255), nullable=True)  # Store the prompt used to generate the image
    
    # Relationship with health record
    record_id = db.Column(db.Integer, db.ForeignKey('health_record.id', ondelete='CASCADE'), nullable=False)
    record = db.relationship('HealthRecord', back_populates='images')

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

class MedicalCondition(db.Model):
    """Model for tracking medical conditions and chronic illnesses"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # Name of the condition
    condition_type = db.Column(db.String(64), nullable=True)  # E.g., 'chronic', 'acute', 'genetic'
    
    # Diagnosis information
    diagnosis_date = db.Column(db.Date, nullable=True)  # When it was diagnosed
    diagnosing_provider = db.Column(db.String(128), nullable=True)  # Who diagnosed it
    
    # Status and severity
    status = db.Column(db.String(64), default='active')  # 'active', 'in_remission', 'resolved'
    severity = db.Column(db.String(64), nullable=True)  # 'mild', 'moderate', 'severe'
    
    # Details
    description = db.Column(db.Text, nullable=True)  # Description of the condition
    symptoms = db.Column(db.Text, nullable=True)  # Common symptoms experienced
    treatment_notes = db.Column(db.Text, nullable=True)  # Notes on treatment approach
    
    # Tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships (optional - for future expansion)
    # medications = db.relationship('Medication', secondary='condition_medications', backref='conditions')
    # appointments = db.relationship('Appointment', secondary='condition_appointments', backref='conditions')
    
    def __repr__(self):
        return f"MedicalCondition('{self.name}', status='{self.status}')"

class HealthGoal(db.Model):
    """Model for tracking health-related goals and progress"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)  # Goal title
    goal_type = db.Column(db.String(64), nullable=False)  # 'weight', 'exercise', 'nutrition', 'medication', 'general', etc.
    
    # Target details
    target_value = db.Column(db.Float, nullable=True)  # Target numeric value (e.g., target weight, exercise minutes)
    target_unit = db.Column(db.String(64), nullable=True)  # Unit of measurement (e.g., lbs, minutes, steps)
    frequency = db.Column(db.String(64), nullable=True)  # Required frequency (e.g., 'daily', '3x per week')
    
    # Description and notes
    description = db.Column(db.Text, nullable=True)  # Detailed goal description
    motivation = db.Column(db.Text, nullable=True)  # Why this goal is important
    action_plan = db.Column(db.Text, nullable=True)  # Steps to achieve the goal
    
    # Timeframes
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    target_date = db.Column(db.Date, nullable=True)  # When goal should be achieved
    
    # Progress tracking
    current_value = db.Column(db.Float, nullable=True)  # Current progress value
    last_updated = db.Column(db.DateTime, nullable=True)  # When progress was last updated
    progress_notes = db.Column(db.Text, nullable=True)  # Notes on progress
    
    # Status tracking
    status = db.Column(db.String(20), nullable=False, default='active')  # 'active', 'completed', 'abandoned'
    completion_date = db.Column(db.Date, nullable=True)  # When goal was achieved
    
    # Creation timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Optional association with related health records
    # related_records = db.relationship('HealthRecord', secondary='goal_records', backref='goals')
    
    def __repr__(self):
        return f"HealthGoal('{self.title}', type='{self.goal_type}', status='{self.status}')"
    
    @property
    def progress_percentage(self):
        """Calculate percentage of goal completion if target value exists"""
        if self.target_value is None or self.current_value is None:
            return None
        
        if self.target_value == 0:
            return 0
            
        # For decreasing goals (like weight loss), invert the calculation
        if self.goal_type == 'weight' and self.current_value > self.target_value:
            # Starting value is needed for weight loss calculation
            starting_value = getattr(self, 'starting_value', self.current_value)
            if starting_value <= self.target_value:
                return 0
            progress = (starting_value - self.current_value) / (starting_value - self.target_value) * 100
        else:
            # For increasing goals (like exercise minutes)
            progress = (self.current_value / self.target_value) * 100
            
        return min(100, max(0, progress))  # Clamp between 0-100%
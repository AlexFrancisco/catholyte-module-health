from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, TextAreaField, BooleanField, SelectField, DateTimeField, DateField
from wtforms.validators import DataRequired, Optional, Length
from flask_wtf.file import FileField, FileAllowed
from datetime import datetime

class MedicationForm(FlaskForm):
    name = StringField('Medication Name', validators=[DataRequired(), Length(max=128)])
    strength = StringField('Strength', validators=[Optional(), Length(max=64)])
    dosage_schedule = StringField('Dosage Schedule', validators=[Optional(), Length(max=128)])
    timing = StringField('Timing', validators=[Optional(), Length(max=128)])
    food_relation = StringField('With/After Food?', validators=[Optional(), Length(max=128)])
    description = TextAreaField('Description', validators=[Optional()])
    pill_description = TextAreaField('Pill Description', validators=[Optional()])
    active = BooleanField('Currently Taking', default=True)
    submit = SubmitField('Save Medication')

class ExerciseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    date = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DietEntryForm(FlaskForm):
    meal_name = StringField('Meal Name', validators=[DataRequired()])
    calories = IntegerField('Calories', validators=[DataRequired()])
    date = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Submit')

class GlucoseReadingForm(FlaskForm):
    level = IntegerField('Glucose Level', validators=[DataRequired()])
    date = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MeasurementForm(FlaskForm):
    weight = FloatField('Weight (kg)', validators=[DataRequired()])
    waist = FloatField('Waist (cm)', validators=[DataRequired()])
    date = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DocumentUploadForm(FlaskForm):
    document = FileField('Medical Document', 
                        validators=[FileAllowed(['csv', 'txt', 'pdf'], 
                        'Only CSV, TXT and PDF files allowed!')])
    submit = SubmitField('Upload Document')

class AppointmentForm(FlaskForm):
    title = StringField('Appointment Title', validators=[DataRequired(), Length(max=128)])
    appointment_type = SelectField('Appointment Type', choices=[
        ('medical', 'Medical'), 
        ('therapy', 'Therapy'),
        ('dental', 'Dental'),
        ('vision', 'Vision/Eye Care'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    provider_name = StringField('Provider Name', validators=[Optional(), Length(max=128)])
    date = DateTimeField('Date & Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[Optional(), Length(max=255)])
    virtual = BooleanField('Virtual Appointment')
    notes = TextAreaField('Notes', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], default='scheduled')
    submit = SubmitField('Save Appointment')

class MedicalConditionForm(FlaskForm):
    name = StringField('Condition Name', validators=[DataRequired(), Length(max=128)])
    condition_type = SelectField('Condition Type', choices=[
        ('', 'Select Type'),
        ('chronic', 'Chronic'),
        ('acute', 'Acute'),
        ('genetic', 'Genetic'),
        ('autoimmune', 'Autoimmune'),
        ('infectious', 'Infectious'),
        ('injury', 'Injury/Trauma'),
        ('mental_health', 'Mental Health'),
        ('other', 'Other')
    ], validators=[Optional()])
    diagnosis_date = DateField('Date of Diagnosis', format='%Y-%m-%d', validators=[Optional()])
    diagnosing_provider = StringField('Diagnosing Provider', validators=[Optional(), Length(max=128)])
    status = SelectField('Current Status', choices=[
        ('active', 'Active'),
        ('in_remission', 'In Remission'),
        ('resolved', 'Resolved')
    ], default='active')
    severity = SelectField('Severity', choices=[
        ('', 'Select Severity'),
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    ], validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    symptoms = TextAreaField('Common Symptoms', validators=[Optional()])
    treatment_notes = TextAreaField('Treatment Notes', validators=[Optional()])
    submit = SubmitField('Save Condition')

class HealthGoalForm(FlaskForm):
    title = StringField('Goal Title', validators=[DataRequired(), Length(max=128)])
    goal_type = SelectField('Goal Type', choices=[
        ('weight', 'Weight Management'),
        ('exercise', 'Exercise/Fitness'),
        ('nutrition', 'Nutrition'),
        ('medication', 'Medication Adherence'),
        ('habit', 'Habit Formation/Breaking'),
        ('sleep', 'Sleep Improvement'),
        ('general', 'General Health'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    
    target_value = FloatField('Target Value (if applicable)', validators=[Optional()])
    target_unit = StringField('Unit of Measurement', validators=[Optional(), Length(max=64)])
    frequency = StringField('Frequency (e.g., daily, 3x per week)', validators=[Optional(), Length(max=64)])
    
    description = TextAreaField('Goal Description', validators=[Optional()])
    motivation = TextAreaField('Motivation (Why is this goal important?)', validators=[Optional()])
    action_plan = TextAreaField('Action Plan (Steps to achieve this goal)', validators=[Optional()])
    
    start_date = DateField('Start Date', format='%Y-%m-%d', default=datetime.utcnow().date(), validators=[DataRequired()])
    target_date = DateField('Target Completion Date', format='%Y-%m-%d', validators=[Optional()])
    
    current_value = FloatField('Current Progress Value', validators=[Optional()])
    progress_notes = TextAreaField('Progress Notes', validators=[Optional()])
    
    status = SelectField('Status', choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned')
    ], default='active')
    
    submit = SubmitField('Save Goal')

class MealPlanForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], default=datetime.now().date())
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={'rows': 15})
    submit = SubmitField('Save')
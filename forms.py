from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, TextAreaField, BooleanField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Optional, Length
from flask_wtf.file import FileField, FileAllowed

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
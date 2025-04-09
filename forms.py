from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

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

class MedicationForm(FlaskForm):
    name = StringField('Medication Name', validators=[DataRequired()])
    dose = StringField('Dose', validators=[DataRequired()])
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
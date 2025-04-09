from flask import render_template, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.modules.health.forms import ExerciseForm, DietEntryForm, GlucoseReadingForm, MedicationForm, MeasurementForm, DocumentUploadForm
from app.modules.health.models import HealthRecord, HealthDocument
from app import db
from datetime import datetime
from app.modules.health import health_tracker_bp
import os
from werkzeug.utils import secure_filename

@health_tracker_bp.route('/exercises', methods=['GET', 'POST'])
@login_required
def exercises():
    form = ExerciseForm()
    if form.validate_on_submit():
        exercise = HealthRecord(
            type='exercise',
            name=form.name.data,
            duration=form.duration.data,
            date=form.date.data,
            user_id=current_user.id  # Set the user_id to the current user's ID
        )
        db.session.add(exercise)
        db.session.commit()
        flash('Exercise added successfully!', 'success')
        return redirect(url_for('health_tracker.exercises'))
    
    # Filter exercises by the current user's ID
    exercises = HealthRecord.query.filter_by(type='exercise', user_id=current_user.id).all()
    return render_template('exercises.html', form=form, exercises=exercises)

@health_tracker_bp.route('/exercises/delete/<int:id>', methods=['POST'])
@login_required
def delete_exercise(id):
    exercise = HealthRecord.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(exercise)
    db.session.commit()
    flash('Exercise deleted successfully!', 'success')
    return redirect(url_for('health_tracker.exercises'))

@health_tracker_bp.route('/diet', methods=['GET', 'POST'])
@login_required
def diet():
    form = DietEntryForm()
    if form.validate_on_submit():
        diet_entry = HealthRecord(
            type='diet',
            name=form.meal_name.data,
            value=form.calories.data,
            date=form.date.data,
            user_id=current_user.id  # Set the user_id to the current user's ID
        )
        db.session.add(diet_entry)
        db.session.commit()
        flash('Diet entry added successfully!', 'success')
        return redirect(url_for('health_tracker.diet'))
    
    # Filter diet entries by the current user's ID
    diet_entries = HealthRecord.query.filter_by(type='diet', user_id=current_user.id).all()
    return render_template('diet.html', form=form, diet_entries=diet_entries)

@health_tracker_bp.route('/diet/delete/<int:id>', methods=['POST'])
@login_required
def delete_diet_entry(id):
    diet_entry = HealthRecord.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(diet_entry)
    db.session.commit()
    flash('Diet entry deleted successfully!', 'success')
    return redirect(url_for('health_tracker.diet'))

@health_tracker_bp.route('/glucose', methods=['GET', 'POST'])
@login_required
def glucose():
    form = GlucoseReadingForm()
    if form.validate_on_submit():
        glucose_reading = HealthRecord(
            type='glucose',
            value=form.level.data,
            date=form.date.data,
            user_id=current_user.id  # Set the user_id to the current user's ID
        )
        db.session.add(glucose_reading)
        db.session.commit()
        flash('Glucose reading added successfully!', 'success')
        return redirect(url_for('health_tracker.glucose'))
    
    # Filter glucose readings by the current user's ID
    glucose_readings = HealthRecord.query.filter_by(type='glucose', user_id=current_user.id).all()
    return render_template('glucose.html', form=form, glucose_readings=glucose_readings)

@health_tracker_bp.route('/glucose/delete/<int:id>', methods=['POST'])
@login_required
def delete_glucose_reading(id):
    glucose_reading = HealthRecord.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(glucose_reading)
    db.session.commit()
    flash('Glucose reading deleted successfully!', 'success')
    return redirect(url_for('health_tracker.glucose'))

@health_tracker_bp.route('/medications', methods=['GET', 'POST'])
@login_required
def medications():
    form = MedicationForm()
    if form.validate_on_submit():
        medication = HealthRecord(
            type='medication',
            name=form.name.data,
            dose=form.dose.data,
            date=form.date.data,
            user_id=current_user.id  # Set the user_id to the current user's ID
        )
        db.session.add(medication)
        db.session.commit()
        flash('Medication added successfully!', 'success')
        return redirect(url_for('health_tracker.medications'))
    
    # Filter medications by the current user's ID
    medications = HealthRecord.query.filter_by(type='medication', user_id=current_user.id).all()
    return render_template('medications.html', form=form, medications=medications)

@health_tracker_bp.route('/medications/delete/<int:id>', methods=['POST'])
@login_required
def delete_medication(id):
    medication = HealthRecord.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(medication)
    db.session.commit()
    flash('Medication deleted successfully!', 'success')
    return redirect(url_for('health_tracker.medications'))

@health_tracker_bp.route('/measurements', methods=['GET', 'POST'])
@login_required
def measurements():
    form = MeasurementForm()
    if form.validate_on_submit():
        measurement = HealthRecord(
            type='measurement',
            value=form.weight.data,
            waist=form.waist.data,
            date=form.date.data,
            user_id=current_user.id  # Set the user_id to the current user's ID
        )
        db.session.add(measurement)
        db.session.commit()
        flash('Measurement added successfully!', 'success')
        return redirect(url_for('health_tracker.measurements'))
    
    # Filter measurements by the current user's ID
    measurements = HealthRecord.query.filter_by(type='measurement', user_id=current_user.id).all()
    return render_template('measurements.html', form=form, measurements=measurements)

@health_tracker_bp.route('/measurements/delete/<int:id>', methods=['POST'])
@login_required
def delete_measurement(id):
    measurement = HealthRecord.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(measurement)
    db.session.commit()
    flash('Measurement deleted successfully!', 'success')
    return redirect(url_for('health_tracker.measurements'))

@health_tracker_bp.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')

@health_tracker_bp.route('/health')
@login_required
def health():
    return render_template('dashboard.html')

@health_tracker_bp.route('/calendar-data')
@login_required
def calendar_data():
    # Fetch diet entries for the current user
    diet_entries = HealthRecord.query.filter_by(type='diet', user_id=current_user.id).all()
    diet_events = [
        {
            'title': f"Meal: {entry.name} ({entry.value} kcal)",
            'start': datetime.strptime(entry.date, '%Y-%m-%d').strftime('%Y-%m-%d'),
            'color': '#28a745'  # Green for diet
        }
        for entry in diet_entries
    ]

    # Fetch exercise entries for the current user
    exercises = HealthRecord.query.filter_by(type='exercise', user_id=current_user.id).all()
    exercise_events = [
        {
            'title': f"Exercise: {entry.name} ({entry.duration} mins)",
            'start': datetime.strptime(entry.date, '%Y-%m-%d').strftime('%Y-%m-%d'),
            'color': '#007bff'  # Blue for exercise
        }
        for entry in exercises
    ]

    # Fetch glucose readings for the current user
    glucose_readings = HealthRecord.query.filter_by(type='glucose', user_id=current_user.id).all()
    glucose_events = [
        {
            'title': f"Glucose: {entry.value} mg/dL",
            'start': datetime.strptime(entry.date, '%Y-%m-%d').strftime('%Y-%m-%d'),
            'color': '#dc3545'  # Red for glucose
        }
        for entry in glucose_readings
    ]

    # Combine all events
    events = diet_events + exercise_events + glucose_events

    return jsonify(events)

@health_tracker_bp.route('/meal-plans', methods=['GET'])
@login_required
def meal_plans():
    """Display meal plans with rendered HTML content."""
    meal_plans = HealthRecord.query.filter_by(
        type='meal plan', 
        user_id=current_user.id
    ).order_by(HealthRecord.date.desc()).all()
    
    return render_template('meal_plans.html', meal_plans=meal_plans)

@health_tracker_bp.route('/meal-plans/delete/<int:id>', methods=['POST'])
@login_required
def delete_meal_plan(id):
    """Delete a meal plan."""
    meal_plan = HealthRecord.query.filter_by(id=id, type='meal_plan', user_id=current_user.id).first_or_404()
    db.session.delete(meal_plan)
    db.session.commit()
    flash('Meal plan deleted successfully!', 'success')
    return redirect(url_for('health_tracker.meal_plans'))

@health_tracker_bp.route('/documents', methods=['GET', 'POST'])
@login_required
def documents():
    form = DocumentUploadForm()
    if form.validate_on_submit():
        file = form.document.data
        if file:
            # Secure filename and save file
            filename = secure_filename(file.filename)
            unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'health_documents', unique_filename)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save file
            file.save(file_path)
            
            # Create document record
            document = HealthDocument(
                filename=unique_filename,
                original_filename=filename,
                file_type=file.filename.split('.')[-1].lower(),
                user_id=current_user.id
            )
            
            db.session.add(document)
            db.session.commit()
            
            # Process the document
            #process_health_document.delay(document.id)
            
            flash('Document uploaded successfully!', 'success')
            return redirect(url_for('health_tracker.documents'))
            
    documents = HealthDocument.query.filter_by(user_id=current_user.id).all()
    return render_template('documents.html', form=form, documents=documents)

@health_tracker_bp.route('/documents/delete/<int:id>', methods=['POST'])
@login_required
def delete_document(id):
    document = HealthDocument.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Delete the physical file
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'health_documents', document.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete the database record
    db.session.delete(document)
    db.session.commit()
    
    flash('Document deleted successfully!', 'success')
    return redirect(url_for('health_tracker.documents'))
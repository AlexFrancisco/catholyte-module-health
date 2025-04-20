from flask import render_template, redirect, url_for, flash, jsonify, current_app, request
from flask_login import login_required, current_user
from app.modules.health.forms import ExerciseForm, DietEntryForm, GlucoseReadingForm, MedicationForm, MeasurementForm, DocumentUploadForm, AppointmentForm, MedicalConditionForm, MealPlanForm
from app.modules.health.models import HealthRecord, HealthDocument, Medication, Appointment, MedicalCondition, HealthRecordImage
from app import db
from datetime import datetime
import json
from app.modules.health import health_tracker_bp
import os
from werkzeug.utils import secure_filename
from app.services.celery_service import celery
# Import the health LLM service

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
    # Get health records for summaries
    health_records = HealthRecord.query.filter_by(user_id=current_user.id).order_by(HealthRecord.date.desc()).all()
    
    # Get medications
    medications = Medication.query.filter_by(user_id=current_user.id).all()
    
    # Get appointments
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    
    meal_plans = HealthRecord.query.filter_by(
        user_id=current_user.id,
        type='meal plan'
    ).order_by(HealthRecord.date.desc()).limit(4).all()
    
    return render_template('dashboard.html',
                          health_records=health_records,
                          medications=medications,
                          appointments=appointments,
                          meal_plans=meal_plans)

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

@health_tracker_bp.route('/medications', methods=['GET', 'POST'])
@login_required
def medications():
    form = MedicationForm()
    if form.validate_on_submit():
        medication = Medication(
            name=form.name.data,
            strength=form.strength.data,
            dosage_schedule=form.dosage_schedule.data,
            timing=form.timing.data,
            food_relation=form.food_relation.data,
            description=form.description.data,
            pill_description=form.pill_description.data,
            active=form.active.data,
            user_id=current_user.id
        )
        db.session.add(medication)
        db.session.commit()
        flash('Medication added successfully!', 'success')
        return redirect(url_for('health.medications'))
    
    # Get all medications for the current user
    medications = Medication.query.filter_by(user_id=current_user.id).order_by(Medication.name).all()
    return render_template('medications.html', form=form, medications=medications)

@health_tracker_bp.route('/medications/<int:medication_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_medication(medication_id):
    medication = Medication.query.filter_by(id=medication_id, user_id=current_user.id).first_or_404()
    form = MedicationForm(obj=medication)
    
    if form.validate_on_submit():
        form.populate_obj(medication)
        db.session.commit()
        flash('Medication updated successfully!', 'success')
        return redirect(url_for('health_tracker.medications'))
    
    return render_template('edit_medication.html', form=form, medication=medication)

@health_tracker_bp.route('/medications/<int:medication_id>/delete', methods=['POST'])
@login_required
def delete_medication(medication_id):
    medication = Medication.query.filter_by(id=medication_id, user_id=current_user.id).first_or_404()
    db.session.delete(medication)
    db.session.commit()
    flash('Medication deleted successfully!', 'success')
    return redirect(url_for('health.medications'))

@health_tracker_bp.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
    form = AppointmentForm()
    
    if form.validate_on_submit():
        appointment = Appointment(
            title=form.title.data,
            appointment_type=form.appointment_type.data,
            provider_name=form.provider_name.data,
            date=form.date.data,
            location=form.location.data,
            virtual=form.virtual.data,
            notes=form.notes.data,
            status=form.status.data,
            user_id=current_user.id
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment added successfully!', 'success')
        return redirect(url_for('health_tracker.appointments'))
    
    # Query appointments based on filters
    status_filter = request.args.get('status', 'all')
    type_filter = request.args.get('type', 'all')
    
    query = Appointment.query.filter_by(user_id=current_user.id)
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
        
    if type_filter != 'all':
        query = query.filter_by(appointment_type=type_filter)
    
    # Sort by date, with upcoming appointments first
    appointments = query.order_by(Appointment.date).all()
    
    return render_template('appointments.html', 
                          appointments=appointments, 
                          form=form,
                          status_filter=status_filter,
                          type_filter=type_filter)

@health_tracker_bp.route('/appointments/<int:appointment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_appointment(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id, user_id=current_user.id).first_or_404()
    form = AppointmentForm(obj=appointment)
    
    if form.validate_on_submit():
        form.populate_obj(appointment)
        db.session.commit()
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('health_tracker.appointments'))
    
    return render_template('edit_appointment.html', form=form, appointment=appointment)

@health_tracker_bp.route('/appointments/<int:appointment_id>/delete', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id, user_id=current_user.id).first_or_404()
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment deleted successfully!', 'success')
    return redirect(url_for('health_tracker.appointments'))

@health_tracker_bp.route('/conditions', methods=['GET', 'POST'])
@login_required
def conditions():
    form = MedicalConditionForm()
    
    if form.validate_on_submit():
        condition = MedicalCondition(
            name=form.name.data,
            condition_type=form.condition_type.data,
            diagnosis_date=form.diagnosis_date.data,
            diagnosing_provider=form.diagnosing_provider.data,
            status=form.status.data,
            severity=form.severity.data,
            description=form.description.data,
            symptoms=form.symptoms.data,
            treatment_notes=form.treatment_notes.data,
            user_id=current_user.id
        )
        db.session.add(condition)
        db.session.commit()
        flash('Medical condition added successfully!', 'success')
        return redirect(url_for('health_tracker.conditions'))
    
    # Get all conditions for the current user
    conditions = MedicalCondition.query.filter_by(user_id=current_user.id).order_by(MedicalCondition.name).all()
    return render_template('conditions.html', form=form, conditions=conditions)

@health_tracker_bp.route('/conditions/<int:condition_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_condition(condition_id):
    condition = MedicalCondition.query.filter_by(id=condition_id, user_id=current_user.id).first_or_404()
    form = MedicalConditionForm(obj=condition)
    
    if form.validate_on_submit():
        form.populate_obj(condition)
        db.session.commit()
        flash('Medical condition updated successfully!', 'success')
        return redirect(url_for('health_tracker.conditions'))
    
    return render_template('edit_condition.html', form=form, condition=condition)

@health_tracker_bp.route('/conditions/<int:condition_id>/delete', methods=['POST'])
@login_required
def delete_condition(condition_id):
    condition = MedicalCondition.query.filter_by(id=condition_id, user_id=current_user.id).first_or_404()
    db.session.delete(condition)
    db.session.commit()
    flash('Medical condition deleted successfully!', 'success')
    return redirect(url_for('health_tracker.conditions'))

@health_tracker_bp.route('/conditions/<int:condition_id>', methods=['GET'])
@login_required
def view_condition(condition_id):
    condition = MedicalCondition.query.filter_by(id=condition_id, user_id=current_user.id).first_or_404()
    return render_template('view_condition.html', condition=condition)

@health_tracker_bp.route('/meal-plans/generate-image/<int:id>', methods=['POST'])
@login_required
def generate_meal_plan_image(id):
    """Generate a new image for a meal plan using the image service."""
    meal_plan = HealthRecord.query.filter_by(id=id, type='meal plan', user_id=current_user.id).first_or_404()
    
    # Create a descriptive prompt for the image generator
    base_prompt = f"Appetizing food photography of {meal_plan.name}. Professional lighting, high-quality image of delicious healthy meal."
    
    # Add variety if there are existing images
    if meal_plan.images:
        # Ensure variety in generated images by modifying prompt slightly
        variation = len(meal_plan.images) % 3
        variations = [
            "Top-down view, on a wooden table. ",
            "Side angle view with natural lighting. ",
            "Close-up shot showing texture and details. "
        ]
        prompt = variations[variation] + base_prompt
    else:
        prompt = base_prompt
    
    # Submit the image generation task
    task = celery.send_task(
        "generate_image",
        args=[prompt],
        kwargs={
            "user_id": current_user.id,
            "entity_type": "meal_plan",
            "entity_id": meal_plan.id,
            "module": "health_tracker",
            "category": "meal_plans"
        }
    )
    task_id = task.id
    
    flash('Image generation has started. Your meal plan image will appear shortly.', 'info')
    return redirect(url_for('health_tracker.meal_plans'))

@health_tracker_bp.route('/api/meal-plans/image-callback/<int:meal_plan_id>', methods=['POST'])
def meal_plan_image_callback(meal_plan_id):
    # Get data from the request
    data = request.json
    image_url = data.get('image_url')
    image_id = data.get('image_id')
    
    meal_plan = MealPlan.query.get_or_404(meal_plan_id)
    
    # Update the meal plan with the image URL
    meal_plan.image_url = image_url
    
    # If we have an image_id, just link to the existing image instead of creating a new one
    if image_id:
        meal_plan.image_id = image_id
        db.session.commit()
        return jsonify({'success': True, 'linked_to_existing': True})
    
    # Otherwise, use your existing code to create a new image record
    # (Only if no image_id is provided from the caller)
    
    return jsonify({'success': True})

@health_tracker_bp.route('/meal-plans/set-primary-image/<int:record_id>/<int:image_id>', methods=['POST'])
@login_required
def set_primary_meal_plan_image(record_id, image_id):
    """Set an image as the primary image for a meal plan."""
    meal_plan = HealthRecord.query.filter_by(id=record_id, type='meal plan', user_id=current_user.id).first_or_404()
    image = HealthRecordImage.query.filter_by(id=image_id, record_id=record_id).first_or_404()
    
    # Reset all images to non-primary
    for img in meal_plan.images:
        img.is_primary = False
    
    # Set the selected image as primary
    image.is_primary = True
    db.session.commit()
    
    flash('Primary image updated successfully.', 'success')
    return redirect(url_for('health_tracker.meal_plans'))

@health_tracker_bp.route('/meal-plans/delete-image/<int:record_id>/<int:image_id>', methods=['POST'])
@login_required
def delete_meal_plan_image(record_id, image_id):
    """Delete an image from a meal plan."""
    meal_plan = HealthRecord.query.filter_by(id=record_id, type='meal plan', user_id=current_user.id).first_or_404()
    image = HealthRecordImage.query.filter_by(id=image_id, record_id=record_id).first_or_404()
    
    was_primary = image.is_primary
    db.session.delete(image)
    
    # If deleted image was primary and other images exist, set a new primary
    if was_primary and meal_plan.images:
        meal_plan.images[0].is_primary = True
    
    db.session.commit()
    
    flash('Image deleted successfully.', 'success')
    return redirect(url_for('health_tracker.meal_plans'))

@health_tracker_bp.route('/meal-plans/create', methods=['GET', 'POST'])
@login_required
def create_meal_plan():
    form = MealPlanForm()
    
    if form.validate_on_submit():
        meal_plan = HealthRecord(
            type='meal plan',
            name=form.name.data,
            date=form.date.data.strftime('%Y-%m-%d'),  # Convert date to string format
            content=form.content.data,
            user_id=current_user.id
        )
        
        db.session.add(meal_plan)
        db.session.commit()
        
        flash('Meal plan created successfully!', 'success')
        return redirect(url_for('health_tracker.meal_plans'))
    
    return render_template('create_meal_plan.html', form=form, title='Create Meal Plan')

@health_tracker_bp.route('/meal-plans/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_meal_plan(id):
    meal_plan = HealthRecord.query.filter_by(id=id, type='meal plan', user_id=current_user.id).first_or_404()
    
    form = MealPlanForm(obj=meal_plan)
    
    if form.validate_on_submit():
        meal_plan.name = form.name.data
        meal_plan.date = form.date.data.strftime('%Y-%m-%d')
        meal_plan.content = form.content.data
        
        db.session.commit()
        
        flash('Meal plan updated successfully!', 'success')
        return redirect(url_for('health_tracker.meal_plans'))
    
    # For GET request, pre-populate the date field
    if request.method == 'GET':
        try:
            form.date.data = datetime.strptime(meal_plan.date, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            form.date.data = datetime.now().date()
    
    return render_template('edit_meal_plan.html', form=form, meal_plan=meal_plan, title='Edit Meal Plan')


def generate_diet_entry_with_llm(meal_description):
    """
    Generate diet entry details using the health LLM service.
    
    Args:
        meal_description: User's description of their meal
        
    Returns:
        dict: Contains meal_name and estimated calories
    """
    # Initialize the health LLM service
    health_llm_service = None
    
    # Use the service to generate diet entry
    return health_llm_service.generate_diet_entry(meal_description)


@health_tracker_bp.route('/diet/generate', methods=['POST'])
@login_required
def generate_diet_entry():
    """Generate a diet entry using LLM based on user description."""
    description = request.form.get('meal_description', '')
    if not description:
        flash('Please provide a meal description.', 'danger')
        return redirect(url_for('health_tracker.diet'))
    
    try:
        # Call LLM service to generate diet entry
        result = generate_diet_entry_with_llm(description)
        
        # Create a form with the generated data
        form = DietEntryForm()
        form.meal_name.data = result['meal_name']
        form.calories.data = result['calories']
        form.date.data = datetime.now().date()
        
        # Get existing diet entries
        diet_entries = HealthRecord.query.filter_by(type='diet', user_id=current_user.id).all()
        
        # Flash success message
        flash(f'Generated diet entry for "{description}". You can edit before saving.', 'success')
        
        # Render the diet page with pre-filled form
        return render_template('diet.html', form=form, diet_entries=diet_entries, 
                              meal_description=description)
    
    except Exception as e:
        flash(f'Error generating diet entry: {str(e)}', 'danger')
        return redirect(url_for('health_tracker.diet'))
from celery import shared_task
from .models import db, Users, Appointments, Doctors, Patients, Treatments
from .extensions import cache
from datetime import datetime, date, timedelta
import requests
import csv
import os
from flask import current_app

GOOGLE_CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQA3X-p3r8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=b8c67ATf0ya8Y7wrxyjaQZut_6tmXfX8NWpjdlMe3Jw"

def send_chat_message(receiver_name, message_body):
    text = f"To: {receiver_name}\n{message_body}"
    try:
        requests.post(GOOGLE_CHAT_WEBHOOK_URL, json={"text": text})
    except Exception as e:
        print(f"Failed to send chat message: {e}")

@shared_task
def send_daily_reminders():
    today = date.today()
    appointments = Appointments.query.filter_by(date=today, status='BOOKED').all()
    
    for appt in appointments:
        patient = appt.patient
        msg = f"Reminder: You have an appointment with Dr. {appt.doctor.user.name} today at {appt.time.strftime('%H:%M')}."
        send_chat_message(patient.user.name, msg)
            
    return f"Sent reminders for {len(appointments)} appointments"

@shared_task
def send_monthly_reports():
    # Calculate stats starting from the beginning of last month
    today = date.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    start_date = last_month.replace(day=1)
    # No end date
    
    doctors = Doctors.query.all()
    
    for doc in doctors:
        # Get appointments for this doctor since start_date
        appts = Appointments.query.filter(
            Appointments.doctor_id == doc.doctor_id,
            Appointments.date >= start_date
        ).all()
        
        total_appts = len(appts)
        completed = len([a for a in appts if a.status == 'COMPLETED'])
        
        msg = (f"Monthly Report (Since {start_date.strftime('%B %Y')}):\n"
               f"Total Appointments: {total_appts}\n"
               f"Completed: {completed}\n"
               f"Cancelled: {total_appts - completed}")
        
        send_chat_message(doc.user.name, msg)
            
    return f"Sent reports to {len(doctors)} doctors"

@shared_task
def export_patient_treatments(patient_id):
    patient = Patients.query.get(patient_id)
    if not patient:
        return "Patient not found"
        
    treatments = Treatments.query.join(Appointments).filter(Appointments.patient_id == patient_id).all()
    
    # Create CSV
    filename = f"treatments_{patient_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    filepath = os.path.join(current_app.root_path, 'static', 'exports', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Doctor', 'Diagnosis', 'Prescription', 'Notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for t in treatments:
            writer.writerow({
                'Date': t.appointment.date,
                'Doctor': t.appointment.doctor.user.name,
                'Diagnosis': t.diagnosis,
                'Prescription': t.prescription,
                'Notes': t.notes
            })
            
    # Send link
    download_link = f"http://localhost:5000/static/exports/{filename}"
    msg = f"Your treatment export is ready. Download here: {download_link}"
    send_chat_message(patient.user.name, msg)
    
    return f"Exported treatments for patient {patient_id}"

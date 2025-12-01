from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from .models import db, Departments, Doctors, Patients, Appointments, Treatments, Prescriptions, Medicine, PrescriptionMed, Users, DoctorAvailability
from .utils import role_required
from .extensions import cache
from .tasks import export_patient_treatments
from datetime import datetime, timedelta, time
from werkzeug.security import generate_password_hash

# --- Departments ---
class DepartmentListResource(Resource):
    @jwt_required()
    @cache.cached(timeout=3600) # Cache for 1 hour
    def get(self):
        depts = Departments.query.all()
        return [{
            "dept_id": d.dept_id,
            "name": d.name,
            "description": d.description,
            "doctors_registered": len(d.doctors)
        } for d in depts], 200

    @jwt_required()
    @role_required(['ADMIN'])
    def post(self):
        data = request.get_json()
        if Departments.query.filter_by(name=data.get('name')).first():
            return {"msg": "Department already exists"}, 400
        
        new_dept = Departments(name=data.get('name'), description=data.get('description'))
        db.session.add(new_dept)
        db.session.commit()
        return {"msg": "Department created"}, 201

class DepartmentResource(Resource):
    @jwt_required()
    def get(self, dept_id):
        d = Departments.query.get_or_404(dept_id)
        return {
            "dept_id": d.dept_id,
            "name": d.name,
            "description": d.description,
            "doctors": [{
                "doctor_id": doc.doctor_id,
                "name": doc.user.name
            } for doc in d.doctors]
        }, 200

    @jwt_required()
    @role_required(['ADMIN'])
    def put(self, dept_id):
        d = Departments.query.get_or_404(dept_id)
        data = request.get_json()
        d.name = data.get('name', d.name)
        d.description = data.get('description', d.description)
        db.session.commit()
        return {"msg": "Department updated"}, 200

    @jwt_required()
    @role_required(['ADMIN'])
    def delete(self, dept_id):
        d = Departments.query.get_or_404(dept_id)
        db.session.delete(d)
        db.session.commit()
        return {"msg": "Department deleted"}, 200

# --- Doctors ---
class DoctorListResource(Resource):
    @jwt_required()
    @cache.cached(timeout=300) # Cache for 5 minutes
    def get(self):
        doctors = Doctors.query.all()
        return [{
            "doctor_id": d.doctor_id,
            "name": d.user.name,
            "email": d.user.email,
            "contact_no": d.user.contact_no,
            "department": d.department.name,
            "dept_id": d.dept_id,
            "qualification": d.qualification,
            "experience_yrs": d.experience_yrs,
            "status": d.user.status,
            "user_id": d.user_id
        } for d in doctors], 200

    @jwt_required()
    @role_required(['ADMIN'])
    def post(self):
        data = request.get_json()
        if Users.query.filter_by(email=data.get('email')).first():
            return {"msg": "Email already exists"}, 400
        
        try:
            # Create User
            new_user = Users(
                name=data.get('name'),
                email=data.get('email'),
                password=generate_password_hash(data.get('password')),
                role='DOCTOR',
                contact_no=data.get('contact_no'),
                status='ACTIVE'
            )
            db.session.add(new_user)
            db.session.flush()

            # Create Doctor Profile
            new_doc = Doctors(
                user_id=new_user.user_id,
                dept_id=data.get('dept_id'),
                experience_yrs=data.get('experience_yrs'),
                qualification=data.get('qualification')
            )
            db.session.add(new_doc)
            
            # Update department count (optional, but good for consistency if not computed)
            # dept = Departments.query.get(data.get('dept_id'))
            # dept.doctors_registered += 1
            
            db.session.commit()
            return {"msg": "Doctor created"}, 201
        except Exception as e:
            db.session.rollback()
            return {"msg": str(e)}, 500

class DoctorResource(Resource):
    @jwt_required()
    def get(self, doctor_id):
        d = Doctors.query.get_or_404(doctor_id)
        return {
            "doctor_id": d.doctor_id,
            "name": d.user.name,
            "email": d.user.email,
            "contact_no": d.user.contact_no,
            "department": d.department.name,
            "dept_id": d.dept_id,
            "qualification": d.qualification,
            "experience_yrs": d.experience_yrs,
            "qualification": d.qualification,
            "experience_yrs": d.experience_yrs,
            "status": d.user.status
        }, 200
    
    @jwt_required()
    def put(self, doctor_id):
        # Admin can update any doctor. Doctor can update their own profile.
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        role = claims.get('role')
        
        d = Doctors.query.get_or_404(doctor_id)
        
        if role != 'ADMIN' and d.user_id != current_user_id:
            return {"msg": "Unauthorized"}, 403

        data = request.get_json()
        
        # Update User details
        if 'name' in data: d.user.name = data['name']
        if 'contact_no' in data: d.user.contact_no = data['contact_no']
        if role == 'ADMIN' and 'status' in data: d.user.status = data['status'] # Only Admin can change status
        
        # Update Doctor details
        if 'qualification' in data: d.qualification = data['qualification']
        if 'experience_yrs' in data: d.experience_yrs = data['experience_yrs']
        if 'experience_yrs' in data: d.experience_yrs = data['experience_yrs']
        if role == 'ADMIN' and 'dept_id' in data: d.dept_id = data['dept_id']


        db.session.commit()
        return {"msg": "Doctor updated"}, 200

    @jwt_required()
    @role_required(['ADMIN'])
    def delete(self, doctor_id):
        d = Doctors.query.get_or_404(doctor_id)
        # We should probably delete the User as well, or just the Doctor profile? 
        # Cascading delete on User will delete Doctor.
        user = d.user
        db.session.delete(user) # This will cascade delete doctor
        db.session.commit()
        return {"msg": "Doctor deleted"}, 200

# --- Patients ---
class PatientListResource(Resource):
    @jwt_required()
    @role_required(['ADMIN', 'DOCTOR'])
    def get(self):
        patients = Patients.query.all()
        return [{
            "patient_id": p.patient_id,
            "name": p.user.name,
            "email": p.user.email,
            "contact_no": p.user.contact_no,
            "gender": p.gender,
            "blood_group": p.blood_group,
            "address": p.address,
            "city": p.city,
            "state": p.state,
            "zip_code": p.zip_code,
            "dob": str(p.date_of_birth),
            "status": p.user.status
        } for p in patients], 200

class PatientResource(Resource):
    @jwt_required()
    def get(self, patient_id):
        # Admin, Doctor, or the Patient themselves
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        role = claims.get('role')
        
        p = Patients.query.get_or_404(patient_id)
        
        if role == 'PATIENT' and p.user_id != current_user_id:
            return {"msg": "Unauthorized"}, 403

        return {
            "patient_id": p.patient_id,
            "name": p.user.name,
            "email": p.user.email,
            "contact_no": p.user.contact_no,
            "gender": p.gender,
            "date_of_birth": str(p.date_of_birth),
            "blood_group": p.blood_group,
            "address": p.address,
            "city": p.city,
            "state": p.state,
            "zip_code": p.zip_code,
            "emergency_contact": p.emergency_contact,
            "allergies": p.allergies,
            "medical_history": p.medical_history,
            "medical_history": p.medical_history,
            "status": p.user.status
        }, 200

    @jwt_required()
    def put(self, patient_id):
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        role = claims.get('role')
        
        p = Patients.query.get_or_404(patient_id)
        
        if role != 'ADMIN' and (role == 'PATIENT' and p.user_id != current_user_id):
             return {"msg": "Unauthorized"}, 403
        
        data = request.get_json()
        
        # Update User fields
        if 'name' in data: p.user.name = data['name']
        if 'contact_no' in data: p.user.contact_no = data['contact_no']
        if role == 'ADMIN' and 'status' in data: p.user.status = data['status']

        # Update Patient fields
        if 'address' in data: p.address = data['address']
        if 'city' in data: p.city = data['city']
        if 'state' in data: p.state = data['state']
        if 'zip_code' in data: p.zip_code = data['zip_code']
        if 'allergies' in data: p.allergies = data['allergies']
        if 'medical_history' in data: p.medical_history = data['medical_history']
        if 'gender' in data: p.gender = data['gender']
        if 'blood_group' in data: p.blood_group = data['blood_group']
        if 'dob' in data and data['dob']:
            try:
                p.date_of_birth = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        db.session.commit()
        return {"msg": "Patient updated"}, 200

    @jwt_required()
    @role_required(['ADMIN'])
    def delete(self, patient_id):
        p = Patients.query.get_or_404(patient_id)
        db.session.delete(p.user) # Cascade
        db.session.commit()
        return {"msg": "Patient deleted"}, 200

# --- Appointments ---
class AppointmentListResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        role = claims.get('role')
        
        query = Appointments.query
        
        if role == 'PATIENT':
            patient = Patients.query.filter_by(user_id=current_user_id).first()
            if not patient: return [], 200
            query = query.filter_by(patient_id=patient.patient_id)
        elif role == 'DOCTOR':
            doctor = Doctors.query.filter_by(user_id=current_user_id).first()
            if not doctor: return [], 200
            query = query.filter_by(doctor_id=doctor.doctor_id)
        
        # Admin sees all
        
        appointments = query.order_by(Appointments.date.desc(), Appointments.time.desc()).all()
        results = []
        for a in appointments:
            appt = {
                "appointment_id": a.appointment_id,
                "patient_name": a.patient.user.name,
                "doctor_name": a.doctor.user.name,
                "doctor_dept": a.doctor.department.name,
                "date": str(a.date),
                "time": str(a.time),
                "status": a.status,
                "reason": a.reason
            }
            if a.treatment:
                appt["treatment"] = {
                    "treatment_id": a.treatment.treatment_id,
                    "diagnosis": a.treatment.diagnosis,
                    "prescription": a.treatment.prescription
                }
            results.append(appt)
        return results, 200

    @jwt_required()
    @role_required(['PATIENT'])
    def post(self):
        current_user_id = int(get_jwt_identity())
        patient = Patients.query.filter_by(user_id=current_user_id).first()
        
        data = request.get_json()
        
        # Check availability (simplified: check if doctor has slot, or just check if not booked)
        # For this project, let's assume we just check if the doctor is free at that time in APPOINTMENTS table
        # Or we can use DOCTOR_AVAILABILITY if implemented. 
        # Let's stick to simple: Check if doctor has appointment at that time.
        
        doctor_id = data.get('doctor_id')
        date_str = data.get('date')
        time_str = data.get('time')
        
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        
        # Check if doctor exists
        if not Doctors.query.get(doctor_id):
            return {"msg": "Doctor not found"}, 404

        # Validate date and time
        try:
            appt_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            appt_time = datetime.strptime(data['time'], '%H:%M').time()
        except ValueError:
            return {"msg": "Invalid date or time format"}, 400

        # Ensure appointment is in the future
        appt_datetime = datetime.combine(appt_date, appt_time)
        if appt_datetime < datetime.now():
            return {"msg": "Cannot book appointments in the past"}, 400

        # Check for double booking (Doctor)
        if Appointments.query.filter_by(doctor_id=data['doctor_id'], date=appt_date, time=appt_time, status='BOOKED').first():
             return {"msg": "Slot already booked"}, 400
             
        # Check for double booking (Patient)
        if Appointments.query.filter_by(patient_id=patient.patient_id, date=appt_date, time=appt_time, status='BOOKED').first():
             return {"msg": "You already have an appointment at this time"}, 400

        new_appt = Appointments(
            patient_id=patient.patient_id,
            doctor_id=data['doctor_id'],
            date=appt_date,
            time=appt_time,
            reason=data.get('reason'),
            status='BOOKED'
        )
        db.session.add(new_appt)
        db.session.commit()
        return {"msg": "Appointment booked"}, 201

class AppointmentResource(Resource):
    @jwt_required()
    def get(self, appointment_id):
        a = Appointments.query.get_or_404(appointment_id)
        # Access control...
        return {
            "appointment_id": a.appointment_id,
            "patient_id": a.patient_id,
            "patient_name": a.patient.user.name,
            "doctor_id": a.doctor_id,
            "doctor_name": a.doctor.user.name,
            "date": str(a.date),
            "time": str(a.time),
            "status": a.status,
            "reason": a.reason
        }, 200

    @jwt_required()
    def put(self, appointment_id):
        # Cancel (Patient) or Update Status (Doctor/Admin)
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        role = claims.get('role')
        
        a = Appointments.query.get_or_404(appointment_id)
        data = request.get_json()
        
        if role == 'PATIENT':
            # Can only cancel
            if a.patient.user_id != current_user_id:
                return {"msg": "Unauthorized"}, 403
            if data.get('status') == 'CANCELLED':
                a.status = 'CANCELLED'
            else:
                return {"msg": "Patients can only cancel appointments"}, 403
        elif role in ['DOCTOR', 'ADMIN']:
            if 'status' in data: a.status = data['status']
        
        db.session.commit()
        return {"msg": "Appointment updated"}, 200

    @jwt_required()
    @role_required(['PATIENT', 'ADMIN'])
    def delete(self, appointment_id):
        # Soft delete or hard delete? Requirement says "Cancel appointment". 
        # Usually PUT status=CANCELLED is better. But if DELETE is requested:
        a = Appointments.query.get_or_404(appointment_id)
        db.session.delete(a)
        db.session.commit()
        return {"msg": "Appointment deleted"}, 200

# --- Treatments ---
class TreatmentResource(Resource):
    @jwt_required()
    def get(self, appointment_id):
        t = Treatments.query.filter_by(appointment_id=appointment_id).first()
        if not t:
            return {}, 200 # Or 404
        return {
            "treatment_id": t.treatment_id,
            "diagnosis": t.diagnosis,
            "prescription": t.prescription,
            "notes": t.notes
        }, 200
    
    @jwt_required()
    @role_required(['DOCTOR'])
    def post(self):
        data = request.get_json()
        appt_id = data.get('appointment_id')
        
        # Check if appointment exists and belongs to doctor
        appt = Appointments.query.get_or_404(appt_id)
        current_user_id = int(get_jwt_identity())
        doctor = Doctors.query.filter_by(user_id=current_user_id).first()
        
        if appt.doctor_id != doctor.doctor_id:
             return {"msg": "Unauthorized"}, 403
             
        # Create or Update
        t = Treatments.query.filter_by(appointment_id=appt_id).first()
        if t:
            t.diagnosis = data.get('diagnosis')
            t.prescription = data.get('prescription')
            t.notes = data.get('notes')
        else:
            t = Treatments(
                appointment_id=appt_id,
                diagnosis=data.get('diagnosis'),
                prescription=data.get('prescription'),
                notes=data.get('notes')
            )
            db.session.add(t)
            
            # Also mark appointment as completed if not already
            appt.status = 'COMPLETED'
            
        db.session.commit()
        return {"msg": "Treatment saved"}, 201

class ExportTreatmentsResource(Resource):
    @jwt_required()
    @role_required(['PATIENT'])
    def post(self):
        current_user_id = int(get_jwt_identity())
        patient = Patients.query.filter_by(user_id=current_user_id).first()
        
        if not patient:
            return {"msg": "Patient not found"}, 404
            
        # Trigger async task
        export_patient_treatments.delay(patient.patient_id)
        
        return {"msg": "Export started. You will receive a link via Google Chat shortly."}, 202

# --- Doctors ---
class DoctorListResource(Resource):
    @jwt_required()
    @cache.cached(timeout=300) # Cache for 5 minutes
    def get(self):
        doctors = Doctors.query.all()
        return [{
            "doctor_id": d.doctor_id,
            "name": d.user.name,
            "email": d.user.email,
            "contact_no": d.user.contact_no,
            "department": d.department.name,
            "dept_id": d.dept_id,
            "qualification": d.qualification,
            "experience_yrs": d.experience_yrs,
            "status": d.user.status,
            "user_id": d.user_id
        } for d in doctors], 200

    @jwt_required()
    @role_required(['ADMIN'])
    def post(self):
        data = request.get_json()
        if Users.query.filter_by(email=data.get('email')).first():
            return {"msg": "Email already exists"}, 400
        
        try:
            # Create User
            new_user = Users(
                name=data.get('name'),
                email=data.get('email'),
                password=generate_password_hash(data.get('password')),
                role='DOCTOR',
                contact_no=data.get('contact_no'),
                status='ACTIVE'
            )
            db.session.add(new_user)
            db.session.flush()

            # Create Doctor Profile
            new_doc = Doctors(
                user_id=new_user.user_id,
                dept_id=data.get('dept_id'),
                experience_yrs=data.get('experience_yrs'),
                qualification=data.get('qualification')
            )
            db.session.add(new_doc)
            
            db.session.commit()
            return {"msg": "Doctor created"}, 201
        except Exception as e:
            db.session.rollback()
            return {"msg": str(e)}, 500

# --- Medicines ---
class MedicineListResource(Resource):
    @jwt_required()
    def get(self):
        meds = Medicine.query.all()
        return [{
            "medicine_id": m.medicine_id,
            "name": m.name,
            "form": m.form,
            "details": m.details
        } for m in meds], 200

    @jwt_required()
    @role_required(['ADMIN'])
    def post(self):
        data = request.get_json()
        if Medicine.query.filter_by(name=data.get('name')).first():
             return {"msg": "Medicine already exists"}, 400
        
        new_med = Medicine(
            name=data.get('name'),
            form=data.get('form'),
            details=data.get('details')
        )
        db.session.add(new_med)
        db.session.commit()
        return {"msg": "Medicine added"}, 201

# --- Stats (Admin Dashboard) ---
class AdminStatsResource(Resource):
    @jwt_required()
    @role_required(['ADMIN'])
    def get(self):
        # Basic Counts
        counts = {
            "doctors": Doctors.query.count(),
            "patients": Patients.query.count(),
            "appointments": Appointments.query.count(),
            "departments": Departments.query.count()
        }
        
        # Appointments by Department
        dept_stats = db.session.query(Departments.name, db.func.count(Appointments.appointment_id))\
            .join(Doctors, Doctors.dept_id == Departments.dept_id)\
            .join(Appointments, Appointments.doctor_id == Doctors.doctor_id)\
            .group_by(Departments.name).all()
        
        # Appointments by Status
        status_stats = db.session.query(Appointments.status, db.func.count(Appointments.appointment_id))\
            .group_by(Appointments.status).all()
            
        # Appointments Last 7 Days
        today = date.today()
        seven_days_ago = today - timedelta(days=6)
        date_stats = db.session.query(Appointments.date, db.func.count(Appointments.appointment_id))\
            .filter(Appointments.date >= seven_days_ago)\
            .group_by(Appointments.date).all()
            
        return {
            "counts": counts,
            "by_department": {name: count for name, count in dept_stats},
            "by_status": {status: count for status, count in status_stats},
            "last_7_days": {str(d): count for d, count in date_stats}
        }, 200

# --- Doctor Availability ---
class DoctorAvailabilityResource(Resource):
    @jwt_required()
    @role_required(['DOCTOR'])
    def get(self):
        current_user_id = int(get_jwt_identity())
        doctor = Doctors.query.filter_by(user_id=current_user_id).first()
        if not doctor:
            return {"msg": "Doctor profile not found"}, 404
            
        # Get availability for next 7 days (or requested range)
        # For simplicity, let's just return all future availability
        today = datetime.now().date()
        availabilities = DoctorAvailability.query.filter(
            DoctorAvailability.doctor_id == doctor.doctor_id,
            DoctorAvailability.date >= today
        ).all()
        
        return [{
            "date": str(a.date),
            "slot_from": str(a.slot_from),
            "slot_to": str(a.slot_to),
            "is_booked": a.is_booked
        } for a in availabilities], 200

    @jwt_required()
    @role_required(['DOCTOR'])
    def post(self):
        current_user_id = int(get_jwt_identity())
        doctor = Doctors.query.filter_by(user_id=current_user_id).first()
        if not doctor:
            return {"msg": "Doctor profile not found"}, 404
            
        data = request.get_json()
        date_str = data.get('date')
        slots = data.get('slots', []) # List of start times e.g. ["09:00", "10:00"]
        
        if not date_str:
            return {"msg": "Date is required"}, 400
            
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Clear existing unbooked slots for this date
        # If a slot is booked, we should probably keep it or error?
        # User requirement: "click on slots to make them available"
        # Let's assume this overwrites availability. 
        # But we must NOT delete booked slots.
        
        existing_slots = DoctorAvailability.query.filter_by(doctor_id=doctor.doctor_id, date=date_obj).all()
        
        # Convert input slots to time objects
        new_slot_times = []
        for s in slots:
            try:
                new_slot_times.append(datetime.strptime(s, '%H:%M').time())
            except ValueError:
                pass # Ignore invalid times
        
        # 1. Remove slots that are NOT in new list AND NOT booked
        for existing in existing_slots:
            if existing.slot_from not in new_slot_times:
                if existing.is_booked:
                    # Warning: User tried to remove a booked slot. We skip deleting it.
                    pass 
                else:
                    db.session.delete(existing)
        
        # 2. Add new slots that don't exist
        existing_start_times = [e.slot_from for e in existing_slots]
        
        for start_time in new_slot_times:
            if start_time not in existing_start_times:
                # Create 1 hour slot
                # Calculate end time
                # Using dummy date to add time
                dummy_dt = datetime.combine(datetime.today(), start_time)
                end_time = (dummy_dt + __import__('datetime').timedelta(hours=1)).time()
                
                new_avail = DoctorAvailability(
                    doctor_id=doctor.doctor_id,
                    date=date_obj,
                    slot_from=start_time,
                    slot_to=end_time,
                    is_booked=0
                )
                db.session.add(new_avail)
                
        db.session.commit()
        return {"msg": "Availability updated"}, 200

class DoctorSlotsResource(Resource):
    @jwt_required()
    def get(self):
        doctor_id = request.args.get('doctor_id')
        date_str = request.args.get('date')

        if not doctor_id or not date_str:
            return {"msg": "Missing doctor_id or date"}, 400

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return {"msg": "Invalid date format"}, 400

        # Check for specific availability
        availabilities = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id,
            date=date_obj
        ).all()

        # Fetch existing appointments for this doctor and date
        # Exclude CANCELLED appointments
        existing_appts = Appointments.query.filter(
            Appointments.doctor_id == doctor_id,
            Appointments.date == date_obj,
            Appointments.status != 'CANCELLED'
        ).all()
        
        booked_times = [a.time for a in existing_appts]

        final_slots = []
        if availabilities:
            # Use defined slots from availability
            for avail in availabilities:
                time_val = avail.slot_from
                is_taken = time_val in booked_times
                final_slots.append({
                    "time": time_val.strftime('%H:%M'),
                    "available": not is_taken
                })
        else:
            # Fallback generation (09:00 - 17:00)
            start_time = datetime.strptime('09:00', '%H:%M').time()
            end_time = datetime.strptime('17:00', '%H:%M').time()
            slot_duration = timedelta(hours=1)
            
            dummy_date = datetime.today().date()
            current_dt = datetime.combine(dummy_date, start_time)
            end_dt = datetime.combine(dummy_date, end_time)

            while current_dt < end_dt:
                time_val = current_dt.time()
                is_taken = time_val in booked_times
                final_slots.append({
                    "time": time_val.strftime('%H:%M'),
                    "available": not is_taken
                })
                current_dt += slot_duration

        # Sort slots by time
        final_slots.sort(key=lambda x: x['time'])
        
        # Filter out past slots if date is today
        now = datetime.now()
        if date_obj == now.date():
            current_time_str = now.strftime('%H:%M')
            # We only want slots strictly greater than current time? 
            # Or maybe give a buffer? The prompt says "if it is already 12:30pm... shouldn't allow booking before 1pm".
            # So strict comparison is fine.
            final_slots = [s for s in final_slots if s['time'] > current_time_str]

        return final_slots, 200

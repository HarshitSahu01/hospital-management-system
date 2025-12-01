from .database import db
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'USERS'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False) # 'ADMIN', 'DOCTOR', 'PATIENT'
    contact_no = db.Column(db.String(15))
    status = db.Column(db.String(20), default='ACTIVE') # 'ACTIVE', 'DISABLED'
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Departments(db.Model):
    __tablename__ = 'DEPARTMENTS'
    dept_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    doctors_registered = db.Column(db.Integer, default=0)
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Doctors(db.Model):
    __tablename__ = 'DOCTORS'
    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.user_id', ondelete='CASCADE'), nullable=False, unique=True)
    dept_id = db.Column(db.Integer, db.ForeignKey('DEPARTMENTS.dept_id', ondelete='SET NULL'), nullable=False)
    experience_yrs = db.Column(db.Integer)
    qualification = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = db.relationship('Users', backref=db.backref('doctor_profile', uselist=False, cascade="all, delete-orphan"))
    department = db.relationship('Departments', backref='doctors')

class Patients(db.Model):
    __tablename__ = 'PATIENTS'
    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.user_id', ondelete='CASCADE'), nullable=False, unique=True)
    gender = db.Column(db.String(10)) # 'Male','Female','Other'
    date_of_birth = db.Column(db.Date)
    blood_group = db.Column(db.String(5))
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(12))
    emergency_contact = db.Column(db.String(15))
    allergies = db.Column(db.String(255))
    medical_history = db.Column(db.Text)
    insurance_id = db.Column(db.String(50))
    insurance_provider = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship('Users', backref=db.backref('patient_profile', uselist=False, cascade="all, delete-orphan"))

class DoctorAvailability(db.Model):
    __tablename__ = 'DOCTOR_AVAILABILITY'
    avail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('DOCTORS.doctor_id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    slot_from = db.Column(db.Time, nullable=False)
    slot_to = db.Column(db.Time, nullable=False)
    is_booked = db.Column(db.Integer, default=0) # 0 or 1
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    doctor = db.relationship('Doctors', backref='availabilities')

class Appointments(db.Model):
    __tablename__ = 'APPOINTMENTS'
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('PATIENTS.patient_id', ondelete='CASCADE'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('DOCTORS.doctor_id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default='BOOKED') # 'BOOKED', 'COMPLETED', 'CANCELLED'
    reason = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    patient = db.relationship('Patients', backref='appointments')
    doctor = db.relationship('Doctors', backref='appointments')
    
    __table_args__ = (
        db.UniqueConstraint('doctor_id', 'date', 'time', name='unique_doctor_appointment'),
        db.UniqueConstraint('patient_id', 'date', 'time', name='unique_patient_appointment'),
    )

class Treatments(db.Model):
    __tablename__ = 'TREATMENTS'
    treatment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('APPOINTMENTS.appointment_id', ondelete='CASCADE'), nullable=False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    appointment = db.relationship('Appointments', backref=db.backref('treatment', uselist=False))

class Prescriptions(db.Model):
    __tablename__ = 'PRESCRIPTIONS'
    prescription_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('APPOINTMENTS.appointment_id', ondelete='CASCADE'), nullable=False)
    prescribed_by = db.Column(db.Integer, db.ForeignKey('DOCTORS.doctor_id', ondelete='SET NULL'))
    notes = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    appointment = db.relationship('Appointments', backref='prescriptions')
    doctor = db.relationship('Doctors')

class Medicine(db.Model):
    __tablename__ = 'MEDICINE'
    medicine_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    form = db.Column(db.String(50)) # 'Tablet','Capsule','Syrup','Injection','Ointment'
    details = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class PrescriptionMed(db.Model):
    __tablename__ = 'PRESCRIPTION_MED'
    pm_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('PRESCRIPTIONS.prescription_id', ondelete='CASCADE'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('MEDICINE.medicine_id', ondelete='CASCADE'), nullable=False)
    dose = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    instructions = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    prescription = db.relationship('Prescriptions', backref='meds')
    medicine = db.relationship('Medicine')
    
    __table_args__ = (db.UniqueConstraint('prescription_id', 'medicine_id', name='unique_prescription_med'),)

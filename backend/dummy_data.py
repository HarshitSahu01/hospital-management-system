from app import create_app, db
from app.models import Users, Departments, Doctors, Patients, Appointments, Medicine
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    print("Creating Admin...")
    if not Users.query.filter_by(email='admin@gmail.com').first():
        admin = Users(
            name='Admin User',
            email='admin@gmail.com',
            password=generate_password_hash('Admin@123'),
            role='ADMIN',
            status='ACTIVE'
        )
        db.session.add(admin)
    
    print("Creating Departments...")
    depts = ['Cardiology', 'Dermatology', 'Neurology', 'Orthopedics', 'Pediatrics']
    dept_objs = []
    for d_name in depts:
        dept = Departments(name=d_name, description=f'Department of {d_name}')
        db.session.add(dept)
        dept_objs.append(dept)
    db.session.flush()
    
    print("Creating Doctors...")
    # Doctor 1
    doc1_user = Users(
        name='Dr. Strange',
        email='strange@gmail.com',
        password=generate_password_hash('password'),
        role='DOCTOR',
        contact_no='1234567890',
        status='ACTIVE'
    )
    db.session.add(doc1_user)
    db.session.flush()
    
    doc1 = Doctors(
        user_id=doc1_user.user_id,
        dept_id=Departments.query.filter_by(name='Neurology').first().dept_id,
        experience_yrs=10,
        qualification='MD Neurology'
    )
    db.session.add(doc1)

    # Doctor 2
    doc2_user = Users(
        name='Dr. House',
        email='house@gmail.com',
        password=generate_password_hash('password'),
        role='DOCTOR',
        contact_no='0987654321',
        status='ACTIVE'
    )
    db.session.add(doc2_user)
    db.session.flush()
    
    doc2 = Doctors(
        user_id=doc2_user.user_id,
        dept_id=Departments.query.filter_by(name='Cardiology').first().dept_id,
        experience_yrs=15,
        qualification='MD Cardiology'
    )
    db.session.add(doc2)
    
    print("Creating Patients...")
    pat1_user = Users(
        name='John Doe',
        email='john@gmail.com',
        password=generate_password_hash('password'),
        role='PATIENT',
        contact_no='1122334455',
        status='ACTIVE'
    )
    db.session.add(pat1_user)
    db.session.flush()
    
    pat1 = Patients(
        user_id=pat1_user.user_id,
        gender='Male',
        date_of_birth=datetime(1990, 1, 1).date(),
        blood_group='O+',
        address='123 Baker St',
        city='London',
        state='UK',
        zip_code='12345'
    )
    db.session.add(pat1)
    
    print("Creating Medicines...")
    meds = [
        ('Paracetamol', 'Tablet', 'For fever'),
        ('Ibuprofen', 'Tablet', 'Painkiller'),
        ('Amoxicillin', 'Capsule', 'Antibiotic'),
        ('Cough Syrup', 'Syrup', 'For cough')
    ]
    for m_name, m_form, m_det in meds:
        med = Medicine(name=m_name, form=m_form, details=m_det)
        db.session.add(med)

    db.session.commit()
    print("Dummy data populated successfully!")

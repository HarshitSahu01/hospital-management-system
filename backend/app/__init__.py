from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from .extensions import db, cache
from .auth import auth_bp
from .models import Users
from .resources import (
    DepartmentListResource, DepartmentResource,
    DoctorListResource, DoctorResource,
    PatientListResource, PatientResource,
    AppointmentListResource, AppointmentResource,
    TreatmentResource, MedicineListResource,
    AdminStatsResource, DoctorAvailabilityResource,
    DoctorSlotsResource, ExportTreatmentsResource
)

from celery import Celery, Task
from celery.schedules import crontab

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def create_app(config_overrides=None):
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key-change-this' # Change in production
    
    # Redis Cache Config
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    
    # Celery Config
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost:6379/0",
            result_backend="redis://localhost:6379/0",
            task_ignore_result=True,
            beat_schedule={
                "daily-reminders": {
                    "task": "app.tasks.send_daily_reminders",
                    "schedule": crontab(hour=8, minute=0), # 8:00 AM Daily
                },
                "monthly-reports": {
                    "task": "app.tasks.send_monthly_reports",
                    "schedule": crontab(day_of_month=1, hour=9, minute=0), # 1st of month 9:00 AM
                },
            },
        ),
    )
    
    if config_overrides:
        app.config.update(config_overrides)
    
    # Initialize Extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    cache.init_app(app)
    celery_init_app(app)
    
    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    from . import resources # Import resources to register routes
    # Setup Flask-RESTful
    api = Api(app, prefix='/api')
    
    # Register Resources
    api.add_resource(DepartmentListResource, '/departments')
    api.add_resource(DepartmentResource, '/departments/<int:dept_id>')
    
    api.add_resource(DoctorListResource, '/doctors')
    api.add_resource(DoctorResource, '/doctors/<int:doctor_id>')
    
    api.add_resource(PatientListResource, '/patients')
    api.add_resource(PatientResource, '/patients/<int:patient_id>')
    
    api.add_resource(AppointmentListResource, '/appointments')
    api.add_resource(AppointmentResource, '/appointments/<int:appointment_id>')
    
    api.add_resource(TreatmentResource, '/treatments', '/treatments/<int:appointment_id>')
    
    api.add_resource(MedicineListResource, '/medicines')
    
    api.add_resource(AdminStatsResource, '/admin/stats')
    api.add_resource(DoctorAvailabilityResource, '/doctor/availability')
    api.add_resource(DoctorSlotsResource, '/doctor/slots')
    api.add_resource(ExportTreatmentsResource, '/export/treatments')
    
    # Create DB Tables
    with app.app_context():
        db.create_all()
        
        # Check if admin exists
        admin = Users.query.filter_by(email='admin@ayurbase.com').first()
        if not admin:
            admin_user = Users(
                name='Admin User',
                email='admin@ayurbase.com',
                password=generate_password_hash('admin123'),
                role='ADMIN',
                status='approved'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created.")
        
    return app

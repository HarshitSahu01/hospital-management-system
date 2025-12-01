from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db
from .models import Users, Patients, Doctors
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Users.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401
    
    if user.status and user.status.upper() == 'DISABLED':
        return jsonify({"msg": "Account is disabled. Please contact admin."}), 403

    # Create tokens
    # Store role in claims
    additional_claims = {"role": user.role}
    access_token = create_access_token(identity=str(user.user_id), additional_claims=additional_claims, expires_delta=timedelta(days=14))
    refresh_token = create_refresh_token(identity=str(user.user_id), additional_claims=additional_claims, expires_delta=timedelta(days=28))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    # Only for Patients. Doctors/Admins are created by Admin or pre-seeded.
    data = request.get_json()
    
    if Users.query.filter_by(email=data.get('email')).first():
        return jsonify({"msg": "Email already exists"}), 400

    try:
        # Create User
        new_user = Users(
            name=data.get('name'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password')),
            role='PATIENT',
            contact_no=data.get('contact_no'),
            status='ACTIVE'
        )
        db.session.add(new_user)
        db.session.flush() # Get user_id

        # Create Patient Profile
        new_patient = Patients(
            user_id=new_user.user_id,
            gender=data.get('gender'),
            date_of_birth=datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date() if data.get('date_of_birth') else None,
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code')
        )
        db.session.add(new_patient)
        db.session.commit()

        return jsonify({"msg": "Patient registered successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Registration failed: {str(e)}"}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "status": user.status
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    # Keep the same role
    additional_claims = {"role": claims.get("role")}
    
    new_access_token = create_access_token(identity=current_user_id, additional_claims=additional_claims, expires_delta=timedelta(days=14))
    
    return jsonify(access_token=new_access_token), 200

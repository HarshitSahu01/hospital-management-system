from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

def role_required(required_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in required_roles:
                return jsonify(msg="Admins only!"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def admin_required():
    return role_required(["ADMIN"])

def doctor_required():
    return role_required(["DOCTOR"])

def patient_required():
    return role_required(["PATIENT"])

import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify, current_app
from app.models import User

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "iat": datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"success": False, "message": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ", 1)[1].strip()
        try:
            payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Token has expired, please log in again"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Invalid token"}), 401

        current_user = User.query.get(payload["user_id"])
        if not current_user:
            return jsonify({"success": False, "message": "User no longer exists"}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @token_required
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if getattr(current_user, "role", "student") != "admin":
            return jsonify({"success": False, "message": "Admin privileges required"}), 403
        return f(current_user, *args, **kwargs)
    return decorated

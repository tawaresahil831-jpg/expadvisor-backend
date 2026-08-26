from flask import Blueprint, request, jsonify
from app.extensions import db, limiter
from app.models import User
from app.utils.auth_utils import generate_token, token_required
from app.utils.validators import validate_length, validate_email

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("100 per hour")
def register():
    data = request.get_json(silent=True) or {}
    errors = {}

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    college = data.get("college")
    branch = data.get("branch")
    year_raw = data.get("year")

    # Name 2-100 chars
    err = validate_length(name, 2, 100, "Name")
    if err: errors["name"] = err

    # Email
    err = validate_email(email)
    if err: errors["email"] = err

    # Password min 6 chars
    err = validate_length(password, 6, 100, "Password")
    if err: errors["password"] = err

    year = None
    if year_raw not in (None, ""):
        try:
            year = int(year_raw)
        except (TypeError, ValueError):
            errors["year"] = "Year must be a number"

    if errors:
        return jsonify({
            "success": False,
            "message": "Validation failed",
            "errors": errors
        }), 400

    email = str(email).strip().lower()

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({
            "success": False,
            "message": "An account with this email already exists"
        }), 409

    new_user = User(
        name=str(name).strip(),
        email=email,
        college=str(college).strip() if college else None,
        branch=str(branch).strip() if branch else None,
        year=year
    )
    new_user.set_password(str(password))

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "data": new_user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

    token = generate_token(user.user_id)

    return jsonify({
        "success": True,
        "message": "Login successful",
        "data": {
            "token": token,
            "user": user.to_dict()
        }
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({
        "success": True,
        "message": "Logged out successfully. Please delete the token on the client side."
    }), 200


@auth_bp.route("/me", methods=["GET"])
@token_required
def get_me(current_user):
    return jsonify({
        "success": True,
        "message": "User fetched successfully",
        "data": current_user.to_dict()
    }), 200

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import string
import random

import uuid
from datetime import datetime, timedelta

@auth_bp.route("/forgot-password", methods=["POST"])
@limiter.limit("5 per hour")
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    
    if not email:
        return jsonify({"success": False, "message": "Email is required"}), 400
        
    user = User.query.filter_by(email=email).first()
    if not user:
        # Prevent email enumeration by returning success anyway
        return jsonify({"success": True, "message": "If an account exists, a reset link was generated."}), 200
        
    # Generate token
    token = str(uuid.uuid4())
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    
    db.session.commit()
    
    reset_link = f"http://localhost:8000/reset_password.html?token={token}"
    print(f"\n=== DEV RESET LINK ===\n{reset_link}\n======================\n")
    
    return jsonify({
        "success": True, 
        "message": "If an account exists, a reset link was generated.",
        "dev_link": reset_link # Exposed only for presentation shortcut
    }), 200

@auth_bp.route("/reset-password", methods=["POST"])
@limiter.limit("5 per hour")
def reset_password():
    data = request.get_json(silent=True) or {}
    token = data.get("token")
    new_password = data.get("password")
    
    if not token or not new_password:
        return jsonify({"success": False, "message": "Token and new password are required"}), 400
        
    if len(new_password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters"}), 400
        
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        return jsonify({"success": False, "message": "Invalid or expired reset token"}), 400
        
    user.set_password(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    
    db.session.commit()
    
    return jsonify({"success": True, "message": "Password has been successfully reset"}), 200

@auth_bp.route("/google", methods=["POST"])
@limiter.limit("20 per minute")
def google_login():
    data = request.get_json(silent=True) or {}
    credential = data.get("credential")
    
    if not credential:
        return jsonify({"success": False, "message": "No credential provided"}), 400
        
    try:
        # Verify the token
        CLIENT_ID = "264177546521-l4f6okrlas9sk890h9elaj17ce6ok5h7.apps.googleusercontent.com"
        idinfo = id_token.verify_oauth2_token(credential, google_requests.Request(), CLIENT_ID)
        
        email = idinfo.get("email")
        name = idinfo.get("name")
        
        if not email:
            return jsonify({"success": False, "message": "Email not found in Google account"}), 400
            
        email = email.lower().strip()
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Create user
            random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            user = User(
                name=name or email.split('@')[0],
                email=email,
                role="student"
            )
            user.set_password(random_password)
            db.session.add(user)
            db.session.commit()
            
        token = generate_token(user.user_id)
        
        return jsonify({
            "success": True,
            "message": "Google Login successful",
            "data": {
                "token": token,
                "user": user.to_dict()
            }
        }), 200
        
    except ValueError as e:
        # Invalid token
        return jsonify({"success": False, "message": "Invalid Google token"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": f"Google auth error: {str(e)}"}), 500

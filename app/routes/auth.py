import random
import string
import uuid
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from app.extensions import db, limiter
from app.models import User
from app.utils.auth_utils import generate_token, token_required
from app.utils.validators import validate_length, validate_email
from app.utils.email_utils import send_otp_email
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

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
    skills = data.get("skills")
    github = data.get("github")
    linkedin = data.get("linkedin")
    portfolio = data.get("portfolio")
    bio = data.get("bio")

    # Name 2-100 chars
    err = validate_length(name, 2, 100, "Name")
    if err: errors["name"] = err

    # Email
    err = validate_email(email)
    if err: errors["email"] = err

    # Password min 6 chars
    err = validate_length(password, 6, 100, "Password")
    if err: errors["password"] = err

    # College (Compulsory)
    err = validate_length(college, 2, 150, "College")
    if err: errors["college"] = "College name is required"

    # Branch (Compulsory)
    err = validate_length(branch, 2, 100, "Branch")
    if err: errors["branch"] = "Branch is required"

    # Year (Compulsory)
    year = None
    if year_raw in (None, ""):
        errors["year"] = "Year of study is required"
    else:
        try:
            s_digits = ''.join(c for c in str(year_raw) if c.isdigit())
            year = int(s_digits) if s_digits else int(year_raw)
        except (TypeError, ValueError):
            errors["year"] = "Year must be a number (e.g. 1, 2, 3, 4)"

    # Skills (Compulsory)
    err = validate_length(skills, 2, 500, "Skills")
    if err: errors["skills"] = "At least one skill is required"

    if errors:
        return jsonify({
            "success": False,
            "message": "Validation failed",
            "errors": errors
        }), 400

    email = str(email).strip().lower()

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        # If user account is already verified, refuse duplicate
        if existing_user.is_verified:
            return jsonify({
                "success": False,
                "message": "An account with this email already exists and is verified. Please sign in."
            }), 409
        else:
            # If account exists but was never verified, reuse and update details
            user = existing_user
            user.name = str(name).strip()
            user.college = str(college).strip() if college else None
            user.branch = str(branch).strip() if branch else None
            user.year = year
            user.skills = str(skills).strip() if skills else None
            user.bio = str(bio).strip() if bio else None
            user.github = str(github).strip() if github else None
            user.linkedin = str(linkedin).strip() if linkedin else None
            user.portfolio = str(portfolio).strip() if portfolio else None
            user.set_password(str(password))
    else:
        user = User(
            name=str(name).strip(),
            email=email,
            college=str(college).strip() if college else None,
            branch=str(branch).strip() if branch else None,
            year=year,
            skills=str(skills).strip() if skills else None,
            bio=str(bio).strip() if bio else None,
            github=str(github).strip() if github else None,
            linkedin=str(linkedin).strip() if linkedin else None,
            portfolio=str(portfolio).strip() if portfolio else None
        )
        user.set_password(str(password))
        db.session.add(user)

    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    user.verification_otp = otp
    user.verification_otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    user.is_verified = False

    db.session.commit()

    # Dispatch OTP email
    send_otp_email(user.email, otp, user.name)

    return jsonify({
        "success": True,
        "requires_verification": True,
        "message": f"A 6-digit verification code has been sent to {user.email}",
        "data": {
            "email": user.email,
            "dev_otp": otp
        }
    }), 201


@auth_bp.route("/verify-otp", methods=["POST"])
@limiter.limit("30 per hour")
def verify_otp():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    otp = str(data.get("otp") or "").strip()

    if not email or not otp:
        return jsonify({
            "success": False,
            "message": "Email and 6-digit verification code are required"
        }), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "User account not found"}), 404

    if user.is_verified:
        token = generate_token(user.user_id)
        return jsonify({
            "success": True,
            "message": "Email is already verified",
            "data": {
                "token": token,
                "user": user.to_dict()
            }
        }), 200

    if not user.verification_otp or user.verification_otp != otp:
        return jsonify({
            "success": False,
            "message": "Invalid verification code. Please check your email and try again."
        }), 400

    if not user.verification_otp_expiry or user.verification_otp_expiry < datetime.utcnow():
        return jsonify({
            "success": False,
            "message": "Verification code has expired. Please request a new code."
        }), 400

    # Mark verified and clear OTP
    user.is_verified = True
    user.verification_otp = None
    user.verification_otp_expiry = None
    db.session.commit()

    token = generate_token(user.user_id)
    user_dict = user.to_dict()
    user_dict["token"] = token

    return jsonify({
        "success": True,
        "message": "Email verified successfully! Welcome to EXPadviser.",
        "data": {
            "token": token,
            "user": user_dict
        }
    }), 200


@auth_bp.route("/resend-otp", methods=["POST"])
@limiter.limit("10 per hour")
def resend_otp():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()

    if not email:
        return jsonify({"success": False, "message": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "User account not found"}), 404

    if user.is_verified:
        return jsonify({"success": False, "message": "Account is already verified. Please sign in."}), 400

    otp = str(random.randint(100000, 999999))
    user.verification_otp = otp
    user.verification_otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()

    send_otp_email(user.email, otp, user.name)

    return jsonify({
        "success": True,
        "message": f"A fresh 6-digit verification code has been sent to {user.email}",
        "data": {
            "email": user.email,
            "dev_otp": otp
        }
    }), 200


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("15 per minute")
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

    # If user account is not verified, require OTP verification before logging in
    if not user.is_verified:
        otp = str(random.randint(100000, 999999))
        user.verification_otp = otp
        user.verification_otp_expiry = datetime.utcnow() + timedelta(minutes=10)
        db.session.commit()

        send_otp_email(user.email, otp, user.name)

        return jsonify({
            "success": False,
            "requires_verification": True,
            "message": "Your email has not been verified yet. We sent a 6-digit verification code to your email.",
            "data": {
                "email": user.email,
                "dev_otp": otp
            }
        }), 403

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


@auth_bp.route("/forgot-password", methods=["POST"])
@limiter.limit("5 per hour")
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    
    if not email:
        return jsonify({"success": False, "message": "Email is required"}), 400
        
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": True, "message": "If an account exists, a reset link was generated."}), 200
        
    token = str(uuid.uuid4())
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    
    db.session.commit()
    
    reset_link = f"http://localhost:8000/reset_password.html?token={token}"
    print(f"\n=== DEV RESET LINK ===\n{reset_link}\n======================\n")
    
    return jsonify({
        "success": True, 
        "message": "If an account exists, a reset link was generated.",
        "dev_link": reset_link
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
        CLIENT_ID = "264177546521-l4f6okrlas9sk890h9elaj17ce6ok5h7.apps.googleusercontent.com"
        idinfo = id_token.verify_oauth2_token(credential, google_requests.Request(), CLIENT_ID)
        
        email = idinfo.get("email")
        name = idinfo.get("name")
        
        if not email:
            return jsonify({"success": False, "message": "Email not found in Google account"}), 400
            
        email = email.lower().strip()
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            user = User(
                name=name or email.split('@')[0],
                email=email,
                role="student",
                is_verified=True
            )
            user.set_password(random_password)
            db.session.add(user)
            db.session.commit()
        else:
            if not user.is_verified:
                user.is_verified = True
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
        return jsonify({"success": False, "message": "Invalid Google token"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": f"Google auth error: {str(e)}"}), 500

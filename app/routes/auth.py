from flask import Blueprint, request, jsonify
from app.extensions import db, limiter
from app.models import User
from app.utils.auth_utils import generate_token, token_required
from app.utils.validators import validate_length, validate_email

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("3 per hour")
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

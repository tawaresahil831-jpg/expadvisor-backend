from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, Experience, Comment
from app.utils.auth_utils import token_required
from app.utils.validators import validate_length
import json

user_bp = Blueprint("user", __name__, url_prefix="/api/users")

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
        
    # Calculate stats
    experiences_count = Experience.query.filter_by(author_id=user_id).count()
    comments_count = Comment.query.filter_by(user_id=user_id).count()
    
    # Simple achievements logic
    achievements = []
    if experiences_count >= 1:
        achievements.append("First Post")
    if experiences_count >= 5:
        achievements.append("Top Solver '24")
    if comments_count >= 10:
        achievements.append("Master Mentor")
    if comments_count >= 1:
        achievements.append("Helper")
        
    user_data = user.to_dict()
    user_data["stats"] = {
        "problems_solved": experiences_count,
        "peers_helped": comments_count
    }
    user_data["achievements"] = achievements

    return jsonify({
        "success": True,
        "message": "User profile fetched successfully",
        "data": user_data
    }), 200

@user_bp.route("/me", methods=["PUT"])
@token_required
def update_my_profile(current_user):
    data = request.get_json(silent=True) or {}
    
    if "name" in data and data.get("name"):
        current_user.name = str(data.get("name")).strip()
        
    if "college" in data:
        current_user.college = str(data.get("college")).strip() if data.get("college") else None
        
    if "branch" in data:
        current_user.branch = str(data.get("branch")).strip() if data.get("branch") else None
        
    if "year" in data:
        y_val = data.get("year")
        if y_val:
            s_digits = ''.join(c for c in str(y_val) if c.isdigit())
            current_user.year = int(s_digits) if s_digits else None
        else:
            current_user.year = None
            
    if "bio" in data:
        bio = data.get("bio")
        if bio:
            err = validate_length(bio, 1, 500, "Bio")
            if err: return jsonify({"success": False, "message": err}), 400
            current_user.bio = bio.strip()
        else:
            current_user.bio = None
            
    if "skills" in data:
        skills = data.get("skills")
        if isinstance(skills, list):
            current_user.skills = ", ".join([s.strip() for s in skills if s.strip()])
        elif isinstance(skills, str):
            current_user.skills = skills.strip()
        else:
            current_user.skills = None

    if "github" in data:
        current_user.github = str(data.get("github")).strip() if data.get("github") else None

    if "linkedin" in data:
        current_user.linkedin = str(data.get("linkedin")).strip() if data.get("linkedin") else None

    if "portfolio" in data:
        current_user.portfolio = str(data.get("portfolio")).strip() if data.get("portfolio") else None
        
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Profile updated successfully",
        "data": current_user.to_dict()
    }), 200

@user_bp.route("/<int:user_id>/activity", methods=["GET"])
def get_user_activity(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
        
    experiences = Experience.query.filter_by(author_id=user_id).all()
    comments = Comment.query.filter_by(user_id=user_id).all()
    
    activity_map = {}
    
    for exp in experiences:
        if exp.created_at:
            date_str = exp.created_at.strftime("%Y-%m-%d")
            activity_map[date_str] = activity_map.get(date_str, 0) + 1
            
    for c in comments:
        if c.created_at:
            date_str = c.created_at.strftime("%Y-%m-%d")
            activity_map[date_str] = activity_map.get(date_str, 0) + 1
            
    return jsonify({
        "success": True,
        "message": "Activity fetched",
        "data": activity_map
    }), 200

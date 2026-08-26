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
    comments_count = Comment.query.filter_by(author_id=user_id).count()
    
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
            current_user.skills = json.dumps(skills)
        elif isinstance(skills, str):
            current_user.skills = skills
        else:
            current_user.skills = None
            
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Profile updated successfully",
        "data": current_user.to_dict()
    }), 200

from flask import Blueprint, jsonify
from app.extensions import db
from app.models import User, Experience, Comment
from app.utils.auth_utils import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.route("/users", methods=["GET"])
@admin_required
def get_users(current_user):
    users = User.query.all()
    return jsonify({
        "success": True,
        "message": "Users fetched successfully",
        "data": [user.to_dict() for user in users]
    }), 200

@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(current_user, user_id):
    if current_user.user_id == user_id:
        return jsonify({
            "success": False,
            "message": "You cannot delete your own admin account"
        }), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": True, "message": "User deleted successfully"}), 200

@admin_bp.route("/experiences/<int:experience_id>", methods=["DELETE"])
@admin_required
def delete_experience(current_user, experience_id):
    experience = Experience.query.get(experience_id)
    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404

    db.session.delete(experience)
    db.session.commit()
    return jsonify({"success": True, "message": "Experience deleted successfully"}), 200

@admin_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
@admin_required
def delete_comment(current_user, comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"success": False, "message": "Comment not found"}), 404

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"success": True, "message": "Comment deleted successfully"}), 200

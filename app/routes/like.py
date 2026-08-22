from flask import Blueprint, jsonify
from app.extensions import db
from app.models import Like, Experience
from app.utils.auth_utils import token_required

like_bp = Blueprint("like", __name__, url_prefix="/api")


@like_bp.route("/experiences/<int:experience_id>/like", methods=["POST"])
@token_required
def like_experience(current_user, experience_id):
    experience = Experience.query.get(experience_id)
    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404

    existing = Like.query.filter_by(experience_id=experience_id, user_id=current_user.user_id).first()
    if existing:
        return jsonify({"success": False, "message": "You already liked this experience"}), 409

    new_like = Like(experience_id=experience_id, user_id=current_user.user_id)
    db.session.add(new_like)
    db.session.commit()

    like_count = Like.query.filter_by(experience_id=experience_id).count()

    return jsonify({
        "success": True,
        "message": "Experience liked successfully",
        "data": {"like_count": like_count}
    }), 201


@like_bp.route("/experiences/<int:experience_id>/like", methods=["DELETE"])
@token_required
def unlike_experience(current_user, experience_id):
    like = Like.query.filter_by(experience_id=experience_id, user_id=current_user.user_id).first()

    if not like:
        return jsonify({"success": False, "message": "You haven't liked this experience"}), 404

    db.session.delete(like)
    db.session.commit()

    like_count = Like.query.filter_by(experience_id=experience_id).count()

    return jsonify({
        "success": True,
        "message": "Like removed successfully",
        "data": {"like_count": like_count}
    }), 200


@like_bp.route("/experiences/<int:experience_id>/likes", methods=["GET"])
def get_like_count(experience_id):
    experience = Experience.query.get(experience_id)
    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404

    like_count = Like.query.filter_by(experience_id=experience_id).count()

    return jsonify({
        "success": True,
        "message": "Like count fetched successfully",
        "data": {"like_count": like_count}
    }), 200
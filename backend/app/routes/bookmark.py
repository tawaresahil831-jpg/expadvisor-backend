from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Bookmark, Experience
from app.utils.auth_utils import token_required

bookmark_bp = Blueprint("bookmark", __name__, url_prefix="/api")

@bookmark_bp.route("/experiences/<int:experience_id>/bookmark", methods=["POST"])
@token_required
def toggle_bookmark(current_user, experience_id):
    experience = Experience.query.get(experience_id)
    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404

    existing = Bookmark.query.filter_by(
        user_id=current_user.user_id,
        experience_id=experience_id
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Experience removed from bookmarks",
            "data": {"is_bookmarked": False}
        }), 200
    else:
        new_bm = Bookmark(user_id=current_user.user_id, experience_id=experience_id)
        db.session.add(new_bm)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Experience bookmarked successfully",
            "data": {"is_bookmarked": True}
        }), 201

@bookmark_bp.route("/bookmarks", methods=["GET"])
@token_required
def get_user_bookmarks(current_user):
    bookmarks = Bookmark.query.filter_by(user_id=current_user.user_id).order_by(Bookmark.created_at.desc()).all()
    return jsonify({
        "success": True,
        "message": "Bookmarks fetched successfully",
        "data": [b.to_dict() for b in bookmarks]
    }), 200

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Comment, Experience
from app.utils.auth_utils import token_required
from app.utils.validators import validate_length

comment_bp = Blueprint("comment", __name__, url_prefix="/api")

@comment_bp.route("/experiences/<int:experience_id>/comments", methods=["GET"])
def get_comments(experience_id):
    experience = Experience.query.get(experience_id)
    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404

    comments = Comment.query.filter_by(experience_id=experience_id).order_by(Comment.created_at.asc()).all()
    return jsonify({
        "success": True,
        "message": "Comments fetched successfully",
        "data": [c.to_dict() for c in comments]
    }), 200

@comment_bp.route("/experiences/<int:experience_id>/comments", methods=["POST"])
@token_required
def add_comment(current_user, experience_id):
    experience = Experience.query.get(experience_id)
    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404

    data = request.get_json(silent=True) or {}
    text = data.get("comment")

    errors = {}
    err = validate_length(text, 1, 1000, "Comment")
    if err:
        errors["comment"] = err

    if errors:
        return jsonify({
            "success": False,
            "message": "Validation failed",
            "errors": errors
        }), 400

    new_comment = Comment(
        experience_id=experience_id,
        user_id=current_user.user_id,
        comment=str(text).strip()
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Comment added successfully",
        "data": new_comment.to_dict()
    }), 201

@comment_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
@token_required
def delete_comment(current_user, comment_id):
    comment = Comment.query.get(comment_id)

    if not comment:
        return jsonify({"success": False, "message": "Comment not found"}), 404

    if comment.user_id != current_user.user_id:
        return jsonify({"success": False, "message": "You are not allowed to delete this comment"}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"success": True, "message": "Comment deleted successfully"}), 200

@comment_bp.route("/comments/<int:comment_id>", methods=["PUT"])
@token_required
def update_comment(current_user, comment_id):
    comment_obj = Comment.query.get(comment_id)

    if not comment_obj:
        return jsonify({"success": False, "message": "Comment not found"}), 404

    if comment_obj.user_id != current_user.user_id:
        return jsonify({"success": False, "message": "You are not allowed to edit this comment"}), 403

    data = request.get_json(silent=True) or {}
    text = data.get("comment")
    
    if not text:
        return jsonify({"success": False, "message": "Validation failed", "errors": {"comment": "Comment cannot be empty"}}), 400

    err = validate_length(text, 1, 1000, "Comment")
    if err:
        return jsonify({"success": False, "message": "Validation failed", "errors": {"comment": err}}), 400

    comment_obj.comment = str(text).strip()
    db.session.commit()

    return jsonify({"success": True, "message": "Comment updated successfully", "data": comment_obj.to_dict()}), 200

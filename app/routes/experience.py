from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Experience
from app.utils.auth_utils import token_required

experience_bp = Blueprint("experience", __name__, url_prefix="/api/experiences")


@experience_bp.route("", methods=["GET"])
def get_experiences():
    experiences = Experience.query.order_by(Experience.created_at.desc()).all()
    return jsonify({
        "success": True,
        "message": "Experiences fetched successfully",
        "data": [exp.to_dict() for exp in experiences]
    }), 200


@experience_bp.route("/<int:experience_id>", methods=["GET"])
def get_experience(experience_id):
    experience = Experience.query.get(experience_id)
    if not experience:
        return jsonify({
            "success": False,
            "message": "Experience not found"
        }), 404
    return jsonify({
        "success": True,
        "message": "Experience fetched successfully",
        "data": experience.to_dict()
    }), 200


@experience_bp.route("", methods=["POST"])
@token_required
def create_experience(current_user):
    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not title or not content:
        return jsonify({
            "success": False,
            "message": "Title and content are required"
        }), 400

    new_experience = Experience(
        title=title,
        content=content,
        category=(data.get("category") or "").strip() or None,
        company=(data.get("company") or "").strip() or None,
        author_id=current_user.user_id,
        semester=(data.get("semester") or "").strip() or None,
        tags=(data.get("tags") or "").strip() or None,
        file_url=(data.get("file_url") or "").strip() or None
    )

    db.session.add(new_experience)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Experience created successfully",
        "data": new_experience.to_dict()
    }), 201


@experience_bp.route("/<int:experience_id>", methods=["PUT"])
@token_required
def update_experience(current_user, experience_id):
    experience = Experience.query.get(experience_id)

    if not experience:
        return jsonify({
            "success": False,
            "message": "Experience not found"
        }), 404

    if experience.author_id != current_user.user_id:
        return jsonify({
            "success": False,
            "message": "You are not allowed to edit this experience"
        }), 403

    data = request.get_json(silent=True) or {}

    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"success": False, "message": "Title cannot be empty"}), 400
        experience.title = title

    if "content" in data:
        content = (data.get("content") or "").strip()
        if not content:
            return jsonify({"success": False, "message": "Content cannot be empty"}), 400
        experience.content = content

    for field in ["category", "company", "semester", "tags", "file_url"]:
        if field in data:
            setattr(experience, field, (data.get(field) or "").strip() or None)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Experience updated successfully",
        "data": experience.to_dict()
    }), 200


@experience_bp.route("/<int:experience_id>", methods=["DELETE"])
@token_required
def delete_experience(current_user, experience_id):
    experience = Experience.query.get(experience_id)

    if not experience:
        return jsonify({
            "success": False,
            "message": "Experience not found"
        }), 404

    if experience.author_id != current_user.user_id:
        return jsonify({
            "success": False,
            "message": "You are not allowed to delete this experience"
        }), 403

    db.session.delete(experience)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Experience deleted successfully"
    }), 200

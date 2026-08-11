from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Experience
from app.utils.auth_utils import token_required

experiences_bp = Blueprint("experiences", __name__, url_prefix="/api/experiences")


def parse_tags(tags):
    if tags is None:
        return None
    if isinstance(tags, list):
        tags = ", ".join(str(t).strip() for t in tags if str(t).strip())
    return tags.strip() if isinstance(tags, str) else None


def serialize_tags(tags):
    if not tags:
        return []
    return [t.strip() for t in tags.split(",") if t.strip()]


def validate_experience_data(data, partial=False):
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not partial and not title:
        return None, None, "Title is required"
    if "title" in data and not title:
        return None, None, "Title is required"
    if "title" in data and len(title) > 200:
        return None, None, "Title must be at most 200 characters"
    if not partial and not content:
        return None, None, "Content is required"
    if "content" in data and not content:
        return None, None, "Content is required"

    return title or None, content or None, None


def experience_dict(experience):
    result = experience.to_dict()
    result["tags"] = serialize_tags(experience.tags)
    return result


@experiences_bp.route("", methods=["POST"])
@token_required
def create_experience(current_user):
    data = request.get_json(silent=True) or {}

    title, content, error = validate_experience_data(data)
    if error:
        return jsonify({"success": False, "message": error}), 400

    new_experience = Experience(
        title=title,
        content=content,
        category=(data.get("category") or "").strip() or None,
        company=(data.get("company") or "").strip() or None,
        author_id=current_user.user_id,
        semester=(data.get("semester") or "").strip() or None,
        tags=parse_tags(data.get("tags")),
        file_url=(data.get("file_url") or "").strip() or None
    )

    db.session.add(new_experience)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Experience created successfully",
        "data": experience_dict(new_experience)
    }), 201


@experiences_bp.route("", methods=["GET"])
def list_experiences():
    experiences = Experience.query.order_by(Experience.created_at.desc()).all()
    return jsonify({
        "success": True,
        "message": "Experiences fetched successfully",
        "data": [experience_dict(e) for e in experiences]
    }), 200


@experiences_bp.route("/<int:experience_id>", methods=["GET"])
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
        "data": experience_dict(experience)
    }), 200


@experiences_bp.route("/<int:experience_id>", methods=["PUT", "PATCH"])
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
            "message": "You can only update your own experiences"
        }), 403

    data = request.get_json(silent=True) or {}

    if "title" in data or "content" in data:
        title, content, error = validate_experience_data(data, partial=True)
        if error:
            return jsonify({"success": False, "message": error}), 400
        if title is not None:
            experience.title = title
        if content is not None:
            experience.content = content

    if "category" in data:
        experience.category = (data.get("category") or "").strip() or None
    if "company" in data:
        experience.company = (data.get("company") or "").strip() or None
    if "semester" in data:
        experience.semester = (data.get("semester") or "").strip() or None
    if "tags" in data:
        experience.tags = parse_tags(data.get("tags"))
    if "file_url" in data:
        experience.file_url = (data.get("file_url") or "").strip() or None

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Experience updated successfully",
        "data": experience_dict(experience)
    }), 200


@experiences_bp.route("/<int:experience_id>", methods=["DELETE"])
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
            "message": "You can only delete your own experiences"
        }), 403

    db.session.delete(experience)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Experience deleted successfully"
    }), 200

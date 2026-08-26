from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from app.extensions import db
from app.models import Experience
from app.utils.auth_utils import token_required
from app.utils.validators import validate_length, validate_choice, validate_semester, ALLOWED_CATEGORIES

experience_bp = Blueprint("experience", __name__, url_prefix="/api/experiences")

@experience_bp.route("", methods=["GET"])
def get_experiences():
    try:
        page = int(request.args.get("page", 1))
        if page < 1: page = 1
    except ValueError:
        page = 1

    try:
        per_page = int(request.args.get("per_page", 10))
        if per_page < 1: per_page = 10
        if per_page > 50: per_page = 50
    except ValueError:
        per_page = 10

    category = request.args.get("category")
    company = request.args.get("company")
    search = request.args.get("search")
    author_id = request.args.get("author_id")

    query = Experience.query

    if author_id:
        try:
            query = query.filter(Experience.author_id == int(author_id))
        except ValueError:
            pass

    if category:
        query = query.filter(Experience.category == category)
    if company:
        query = query.filter(Experience.company == company)
    if search and search.strip():
        search_term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Experience.title.ilike(search_term),
                Experience.content.ilike(search_term)
            )
        )

    paginated_experiences = query.order_by(Experience.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "success": True,
        "message": "Experiences fetched successfully",
        "data": [exp.to_dict() for exp in paginated_experiences.items],
        "pagination": {
            "page": paginated_experiences.page,
            "per_page": paginated_experiences.per_page,
            "total_items": paginated_experiences.total,
            "total_pages": paginated_experiences.pages,
            "has_next": paginated_experiences.has_next,
            "has_prev": paginated_experiences.has_prev
        }
    }), 200

@experience_bp.route("/<int:experience_id>", methods=["GET"])
def get_experience(experience_id):
    experience = Experience.query.get(experience_id)
    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404
        
    # Increment views
    if experience.views is None:
        experience.views = 0
    experience.views += 1
    db.session.commit()
    return jsonify({"success": True, "message": "Experience fetched successfully", "data": experience.to_dict()}), 200

@experience_bp.route("", methods=["POST"])
@token_required
def create_experience(current_user):
    data = request.get_json(silent=True) or {}
    errors = {}

    title = data.get("title")
    content = data.get("content")
    category = data.get("category")
    semester = data.get("semester")

    err = validate_length(title, 5, 200, "Title")
    if err: errors["title"] = err

    err = validate_length(content, 20, 50000, "Content")
    if err: errors["content"] = err

    if category is not None:
        err = validate_choice(category, ALLOWED_CATEGORIES, "Category")
        if err: errors["category"] = err

    if semester is not None:
        err = validate_semester(semester)
        if err: errors["semester"] = err

    if errors:
        return jsonify({"success": False, "message": "Validation failed", "errors": errors}), 400

    new_experience = Experience(
        title=str(title).strip(),
        content=str(content).strip(),
        category=str(category).strip() if category else None,
        company=(data.get("company") or "").strip() or None,
        author_id=current_user.user_id,
        semester=str(semester).strip() if semester else None,
        tags=(data.get("tags") or "").strip() or None,
        file_url=(data.get("file_url") or "").strip() or None
    )

    db.session.add(new_experience)
    db.session.commit()

    return jsonify({"success": True, "message": "Experience created successfully", "data": new_experience.to_dict()}), 201

@experience_bp.route("/<int:experience_id>", methods=["PUT"])
@token_required
def update_experience(current_user, experience_id):
    experience = Experience.query.get(experience_id)

    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404

    if experience.author_id != current_user.user_id:
        return jsonify({"success": False, "message": "You are not allowed to edit this experience"}), 403

    data = request.get_json(silent=True) or {}
    errors = {}

    if "title" in data:
        err = validate_length(data.get("title"), 5, 200, "Title")
        if err: errors["title"] = err
        else: experience.title = str(data.get("title")).strip()

    if "content" in data:
        err = validate_length(data.get("content"), 20, 50000, "Content")
        if err: errors["content"] = err
        else: experience.content = str(data.get("content")).strip()

    if "category" in data:
        err = validate_choice(data.get("category"), ALLOWED_CATEGORIES, "Category")
        if err: errors["category"] = err
        else: experience.category = str(data.get("category")).strip() if data.get("category") else None

    if "semester" in data:
        err = validate_semester(data.get("semester"))
        if err: errors["semester"] = err
        else: experience.semester = str(data.get("semester")).strip() if data.get("semester") else None

    if errors:
        return jsonify({"success": False, "message": "Validation failed", "errors": errors}), 400

    for field in ["company", "tags", "file_url"]:
        if field in data:
            setattr(experience, field, (data.get(field) or "").strip() or None)

    db.session.commit()

    return jsonify({"success": True, "message": "Experience updated successfully", "data": experience.to_dict()}), 200

@experience_bp.route("/<int:experience_id>", methods=["DELETE"])
@token_required
def delete_experience(current_user, experience_id):
    experience = Experience.query.get(experience_id)

    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404

    if experience.author_id != current_user.user_id:
        return jsonify({"success": False, "message": "You are not allowed to delete this experience"}), 403

    db.session.delete(experience)
    db.session.commit()

    return jsonify({"success": True, "message": "Experience deleted successfully"}), 200

from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from app.extensions import db
from app.models import Experience, User, Comment, Like
from app.utils.auth_utils import token_required
from app.utils.validators import validate_length, validate_choice, validate_semester, ALLOWED_CATEGORIES

experience_bp = Blueprint("experience", __name__, url_prefix="/api/experiences")

@experience_bp.route("/stats", methods=["GET"])
def get_community_stats():
    try:
        total_queries = Experience.query.count()
        answered_queries = Experience.query.filter(Experience.is_resolved == True).count()
        members_count = User.query.count()
        contributors_count = db.session.query(db.func.count(db.func.distinct(Comment.user_id))).scalar() or 0

        return jsonify({
            "success": True,
            "data": {
                "total_queries": total_queries,
                "answered": answered_queries,
                "members": members_count,
                "contributors": contributors_count
            }
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@experience_bp.route("/trending", methods=["GET"])
def get_trending_experience():
    try:
        all_experiences = Experience.query.all()
        if not all_experiences:
            return jsonify({"success": True, "data": None}), 200

        def score(exp):
            views = exp.views or 0
            comments = len(exp.comments) if hasattr(exp, 'comments') and exp.comments else 0
            likes = len(exp.likes) if hasattr(exp, 'likes') and exp.likes else 0
            return views + (comments * 3) + (likes * 2)

        trending = max(all_experiences, key=score)

        participants = []
        seen_ids = set()
        if trending.author:
            seen_ids.add(trending.author.user_id)
            participants.append({
                "user_id": trending.author.user_id,
                "name": trending.author.name or "User",
                "initial": (trending.author.name or "U")[0].upper(),
                "avatar_url": getattr(trending.author, 'avatar_url', None)
            })

        for c in trending.comments:
            if c.user and c.user.user_id not in seen_ids:
                seen_ids.add(c.user.user_id)
                participants.append({
                    "user_id": c.user.user_id,
                    "name": c.user.name or "User",
                    "initial": (c.user.name or "U")[0].upper(),
                    "avatar_url": getattr(c.user, 'avatar_url', None)
                })
            if len(participants) >= 3:
                break

        trending_data = trending.to_dict()
        trending_data["participants"] = participants

        return jsonify({
            "success": True,
            "data": trending_data
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

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

    STANDARD_CATEGORIES = ['project', 'course', 'internship', 'placement', 'tech', 'career', 'design']

    if category and category.strip():
        cat_clean = category.strip().lower()
        if cat_clean == 'other':
            query = query.filter(
                or_(
                    Experience.category.ilike('other'),
                    Experience.category.is_(None),
                    Experience.category.like('#%'),
                    ~db.func.lower(Experience.category).in_(STANDARD_CATEGORIES)
                )
            )
        else:
            clean_name = cat_clean.lstrip('#')
            query = query.filter(
                or_(
                    Experience.category.ilike(cat_clean),
                    Experience.category.ilike(clean_name),
                    Experience.category.ilike(f"#{clean_name}")
                )
            )
    if company:
        query = query.filter(Experience.company == company)
    if search and search.strip():
        raw_term = search.strip()
        clean_term = raw_term.lstrip('#')
        search_patterns = [f"%{raw_term}%"]
        if clean_term and clean_term != raw_term:
            search_patterns.append(f"%{clean_term}%")

        search_filters = []
        for pat in search_patterns:
            search_filters.extend([
                Experience.title.ilike(pat),
                Experience.content.ilike(pat),
                Experience.category.ilike(pat),
                Experience.tags.ilike(pat),
                Experience.company.ilike(pat)
            ])
        query = query.filter(or_(*search_filters))

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

    if semester is not None:
        s_clean = str(semester).strip()
        sem_map = {"1": "1st", "2": "2nd", "3": "3rd", "4": "4th", "5": "5th", "6": "6th", "7": "7th", "8": "8th"}
        semester = sem_map.get(s_clean, s_clean)

    err = validate_length(title, 3, 200, "Title")
    if err: errors["title"] = err

    err = validate_length(content, 3, 50000, "Content")
    if err: errors["content"] = err

    if category is not None and str(category).strip():
        err = validate_length(str(category).strip(), 1, 50, "Category")
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
        val = data.get("category")
        if val and str(val).strip():
            err = validate_length(str(val).strip(), 1, 50, "Category")
            if err: errors["category"] = err
            else: experience.category = str(val).strip()
        else:
            experience.category = None

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

    try:
        from app.models.comment import Comment
        from app.models.like import Like
        from app.models.notification import Notification

        Comment.query.filter_by(experience_id=experience_id).delete()
        Like.query.filter_by(experience_id=experience_id).delete()
        Notification.query.filter_by(experience_id=experience_id).delete()

        db.session.delete(experience)
        db.session.commit()
        return jsonify({"success": True, "message": "Experience deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Failed to delete experience: {str(e)}"}), 500

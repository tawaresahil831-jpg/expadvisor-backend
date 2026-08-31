from flask import Blueprint, jsonify
from app.extensions import db
from app.models import Notification
from app.utils.auth_utils import token_required

notification_bp = Blueprint("notification", __name__, url_prefix="/api")

@notification_bp.route("/notifications", methods=["GET"])
@token_required
def get_notifications(current_user):
    notifications = Notification.query.filter_by(user_id=current_user.user_id).order_by(Notification.created_at.desc()).limit(30).all()
    
    # If user has no notifications yet, provide an initial welcome notification
    if not notifications:
        welcome_notif = Notification(
            user_id=current_user.user_id,
            actor_id=None,
            experience_id=None,
            message=f"Welcome to EXPadviser, {current_user.name}! 🚀 Ask queries, solve coursework doubts, and unlock achievement badges.",
            is_read=False
        )
        db.session.add(welcome_notif)
        db.session.commit()
        notifications = [welcome_notif]

    return jsonify({
        "success": True,
        "message": "Notifications fetched successfully",
        "data": [n.to_dict() for n in notifications]
    }), 200

@notification_bp.route("/notifications/<int:notif_id>/read", methods=["PUT"])
@token_required
def read_notification(current_user, notif_id):
    notif = Notification.query.get(notif_id)
    if not notif:
        return jsonify({"success": False, "message": "Notification not found"}), 404
        
    if notif.user_id != current_user.user_id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
        
    notif.is_read = True
    db.session.commit()
    
    return jsonify({"success": True, "message": "Notification marked as read"}), 200

@notification_bp.route("/notifications/read-all", methods=["PUT"])
@notification_bp.route("/notifications/read", methods=["PUT"])
@token_required
def mark_all_read(current_user):
    Notification.query.filter_by(user_id=current_user.user_id, is_read=False).update({"is_read": True})
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "All notifications marked as read"
    }), 200

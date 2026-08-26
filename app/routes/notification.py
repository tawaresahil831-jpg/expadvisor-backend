from flask import Blueprint, jsonify
from app.extensions import db
from app.models import Notification
from app.utils.auth_utils import token_required

notification_bp = Blueprint("notification", __name__, url_prefix="/api")

@notification_bp.route("/notifications", methods=["GET"])
@token_required
def get_notifications(current_user):
    notifications = Notification.query.filter_by(user_id=current_user.user_id).order_by(Notification.created_at.desc()).limit(20).all()
    
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

import os
import sys

sys.path.insert(0, '/Users/sahiltaware415/expadvisor-backend')

# 1. Update comment.py
comment_path = '/Users/sahiltaware415/expadvisor-backend/app/routes/comment.py'
with open(comment_path, 'r') as f:
    content = f.read()

if 'from app.models import Comment, Experience, Notification' not in content:
    content = content.replace('from app.models import Comment, Experience', 'from app.models import Comment, Experience, Notification')

    # Add notification logic inside add_comment
    # We find where db.session.commit() is for the new comment
    insert_idx = content.find('db.session.add(new_comment)\n    db.session.commit()')
    
    if insert_idx != -1:
        notification_logic = """db.session.add(new_comment)
    
    # Create notification if someone else commented
    if experience.author_id != current_user.user_id:
        notif = Notification(
            user_id=experience.author_id,
            actor_id=current_user.user_id,
            experience_id=experience.experience_id,
            message=f"{current_user.name} commented on your post."
        )
        db.session.add(notif)
        
    db.session.commit()"""
        content = content[:insert_idx] + notification_logic + content[insert_idx + len('db.session.add(new_comment)\n    db.session.commit()'):]

    with open(comment_path, 'w') as f:
        f.write(content)


# 2. Create app/routes/notification.py
notif_code = """from flask import Blueprint, jsonify
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
"""

with open('/Users/sahiltaware415/expadvisor-backend/app/routes/notification.py', 'w') as f:
    f.write(notif_code)

# 3. Register in __init__.py
init_path = '/Users/sahiltaware415/expadvisor-backend/app/__init__.py'
with open(init_path, 'r') as f:
    init_content = f.read()

if 'from .routes.notification import notification_bp' not in init_content:
    # insert before return app
    insert_str = """
    from .routes.notification import notification_bp
    app.register_blueprint(notification_bp)
    
    return app"""
    init_content = init_content.replace('return app', insert_str)
    with open(init_path, 'w') as f:
        f.write(init_content)

print("Patched comment.py and created notification.py")


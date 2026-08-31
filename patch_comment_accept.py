import os
import sys

filepath = '/Users/sahiltaware415/expadvisor-backend/app/routes/comment.py'
with open(filepath, 'r') as f:
    content = f.read()

accept_route = """
@comment_bp.route("/comments/<int:comment_id>/accept", methods=["PUT"])
@token_required
def accept_comment(current_user, comment_id):
    comment_obj = Comment.query.get(comment_id)
    if not comment_obj:
        return jsonify({"success": False, "message": "Comment not found"}), 404

    experience = Experience.query.get(comment_obj.experience_id)
    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404

    if experience.author_id != current_user.user_id:
        return jsonify({"success": False, "message": "Only the query owner can accept a solution"}), 403

    # Mark all other comments as not accepted, and this one as accepted
    for c in experience.comments:
        c.is_accepted = False
    
    comment_obj.is_accepted = True
    experience.is_resolved = True

    # Send notification to the comment author if it's not the owner themselves
    if comment_obj.user_id != current_user.user_id:
        # Check if Notification model is imported, if not it was imported at top
        from app.models import Notification
        notif = Notification(
            user_id=comment_obj.user_id,
            actor_id=current_user.user_id,
            experience_id=experience.experience_id,
            message=f"{current_user.name} accepted your comment as the solution."
        )
        db.session.add(notif)

    db.session.commit()

    return jsonify({"success": True, "message": "Solution accepted successfully"}), 200
"""

if 'def accept_comment' not in content:
    content += accept_route
    with open(filepath, 'w') as f:
        f.write(content)
    print("Added accept_comment route.")
else:
    print("Route already exists.")

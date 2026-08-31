import re

filepath = '/Users/sahiltaware415/expadvisor-backend/app/routes/user.py'
with open(filepath, 'r') as f:
    content = f.read()

if 'def get_user_activity' not in content:
    activity_route = """
@user_bp.route("/<int:user_id>/activity", methods=["GET"])
def get_user_activity(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
        
    experiences = Experience.query.filter_by(author_id=user_id).all()
    comments = Comment.query.filter_by(user_id=user_id).all()
    
    activity_map = {}
    
    for exp in experiences:
        if exp.created_at:
            date_str = exp.created_at.strftime("%Y-%m-%d")
            activity_map[date_str] = activity_map.get(date_str, 0) + 1
            
    for c in comments:
        if c.created_at:
            date_str = c.created_at.strftime("%Y-%m-%d")
            activity_map[date_str] = activity_map.get(date_str, 0) + 1
            
    return jsonify({
        "success": True,
        "message": "Activity fetched",
        "data": activity_map
    }), 200
"""
    content += activity_route

with open(filepath, 'w') as f:
    f.write(content)

print("Patched app/routes/user.py")

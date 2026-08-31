import os

with open("app/routes/auth.py", "r") as f:
    content = f.read()

new_routes = """
import uuid
from datetime import datetime, timedelta

@auth_bp.route("/forgot-password", methods=["POST"])
@limiter.limit("5 per hour")
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    
    if not email:
        return jsonify({"success": False, "message": "Email is required"}), 400
        
    user = User.query.filter_by(email=email).first()
    if not user:
        # Prevent email enumeration by returning success anyway
        return jsonify({"success": True, "message": "If an account exists, a reset link was generated."}), 200
        
    # Generate token
    token = str(uuid.uuid4())
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    
    db.session.commit()
    
    reset_link = f"http://localhost:8000/reset_password.html?token={token}"
    print(f"\\n=== DEV RESET LINK ===\\n{reset_link}\\n======================\\n")
    
    return jsonify({
        "success": True, 
        "message": "If an account exists, a reset link was generated.",
        "dev_link": reset_link # Exposed only for presentation shortcut
    }), 200

@auth_bp.route("/reset-password", methods=["POST"])
@limiter.limit("5 per hour")
def reset_password():
    data = request.get_json(silent=True) or {}
    token = data.get("token")
    new_password = data.get("password")
    
    if not token or not new_password:
        return jsonify({"success": False, "message": "Token and new password are required"}), 400
        
    if len(new_password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters"}), 400
        
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        return jsonify({"success": False, "message": "Invalid or expired reset token"}), 400
        
    user.set_password(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    
    db.session.commit()
    
    return jsonify({"success": True, "message": "Password has been successfully reset"}), 200
"""

if "/forgot-password" not in content:
    # Append the new routes at the end of the file
    content += new_routes
    with open("app/routes/auth.py", "w") as f:
        f.write(content)
    print("Patched auth.py")
else:
    print("Already patched.")

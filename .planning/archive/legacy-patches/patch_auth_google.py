import re

with open('/Users/sahiltaware415/expadvisor-backend/app/routes/auth.py', 'r') as f:
    content = f.read()

# Add imports
imports = """from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import string
import random
"""

if 'from google.oauth2 import id_token' not in content:
    content = content.replace('import uuid', imports + '\nimport uuid')
    
# Add the google route
google_route = """
@auth_bp.route("/google", methods=["POST"])
@limiter.limit("20 per minute")
def google_login():
    data = request.get_json(silent=True) or {}
    credential = data.get("credential")
    
    if not credential:
        return jsonify({"success": False, "message": "No credential provided"}), 400
        
    try:
        # Verify the token
        CLIENT_ID = "264177546521-l4f6okrlas9sk890h9elaj17ce6ok5h7.apps.googleusercontent.com"
        idinfo = id_token.verify_oauth2_token(credential, google_requests.Request(), CLIENT_ID)
        
        email = idinfo.get("email")
        name = idinfo.get("name")
        
        if not email:
            return jsonify({"success": False, "message": "Email not found in Google account"}), 400
            
        email = email.lower().strip()
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Create user
            random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            user = User(
                name=name or email.split('@')[0],
                email=email,
                role="student"
            )
            user.set_password(random_password)
            db.session.add(user)
            db.session.commit()
            
        token = generate_token(user.user_id)
        
        return jsonify({
            "success": True,
            "message": "Google Login successful",
            "data": {
                "token": token,
                "user": user.to_dict()
            }
        }), 200
        
    except ValueError as e:
        # Invalid token
        return jsonify({"success": False, "message": "Invalid Google token"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": f"Google auth error: {str(e)}"}), 500
"""

if 'def google_login():' not in content:
    content = content + google_route
    with open('/Users/sahiltaware415/expadvisor-backend/app/routes/auth.py', 'w') as f:
        f.write(content)
    print("Backend auth patched.")
else:
    print("Backend auth already patched.")

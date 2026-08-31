with open('/Users/sahiltaware415/expadvisor-backend/app/routes/experience.py', 'r') as f:
    content = f.read()

target = """def get_experience(experience_id):
    experience = Experience.query.get(experience_id)
    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404"""

replacement = """def get_experience(experience_id):
    experience = Experience.query.get(experience_id)
    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404
        
    # Increment views
    if experience.views is None:
        experience.views = 0
    experience.views += 1
    db.session.commit()"""

if target in content and 'experience.views += 1' not in content:
    content = content.replace(target, replacement)
    with open('/Users/sahiltaware415/expadvisor-backend/app/routes/experience.py', 'w') as f:
        f.write(content)
    print("Experience route patched successfully.")
else:
    print("Target not found or already patched.")

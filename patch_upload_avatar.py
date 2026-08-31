import re

filepath = '/Users/sahiltaware415/expadvisor-backend/app/routes/upload.py'
with open(filepath, 'r') as f:
    content = f.read()

# Add the new route to upload.py
if '@upload_bp.route("/users/me/avatar"' not in content:
    avatar_route = """
@upload_bp.route("/users/me/avatar", methods=["POST"])
@token_required
def upload_avatar(current_user):
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file part in the request"}), 400
        
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"success": False, "message": "No selected file"}), 400
        
    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "File type not allowed. Allowed types: pdf, png, jpg, jpeg"}), 400
        
    file.seek(0, os.SEEK_END)
    size = file.tell()
    if size > MAX_FILE_SIZE:
        return jsonify({"success": False, "message": "File too large. Maximum size is 5MB"}), 400
    file.seek(0)
    
    supabase_url = current_app.config.get("SUPABASE_URL")
    supabase_key = current_app.config.get("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        return jsonify({"success": False, "message": "Supabase credentials not configured"}), 500
        
    supabase: Client = create_client(supabase_url, supabase_key)
    file_bytes = file.read()
    
    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_filename = f"avatars/{uuid.uuid4().hex}.{ext}"
    
    try:
        supabase.storage.from_("experience-files").upload(
            file=file_bytes,
            path=unique_filename,
            file_options={"content-type": file.content_type}
        )
        
        public_url = supabase.storage.from_("experience-files").get_public_url(unique_filename)
        
        current_user.avatar_url = public_url
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Avatar uploaded successfully",
            "data": current_user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"File upload failed: {str(e)}"
        }), 500
"""
    content += avatar_route

with open(filepath, 'w') as f:
    f.write(content)

print("Patched app/routes/upload.py")

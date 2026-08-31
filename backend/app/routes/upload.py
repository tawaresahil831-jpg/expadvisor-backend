import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from supabase import create_client, Client
from app.extensions import db
from app.models import Experience
from app.utils.auth_utils import token_required

upload_bp = Blueprint("upload", __name__, url_prefix="/api")

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024 # 5 MB

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/experiences/<int:experience_id>/upload", methods=["POST"])
@token_required
def upload_file(current_user, experience_id):
    experience = Experience.query.get(experience_id)
    
    if not experience:
        return jsonify({"success": False, "message": "Experience not found"}), 404

    if experience.author_id != current_user.user_id:
        return jsonify({"success": False, "message": "You are not allowed to edit this experience"}), 403

    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file part in the request"}), 400
        
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"success": False, "message": "No selected file"}), 400
        
    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "File type not allowed. Allowed types: pdf, png, jpg, jpeg"}), 400
        
    # Check size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    if size > MAX_FILE_SIZE:
        return jsonify({"success": False, "message": "File too large. Maximum size is 5MB"}), 400
    file.seek(0)
    
    # Init supabase client
    supabase_url = current_app.config.get("SUPABASE_URL")
    supabase_key = current_app.config.get("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        return jsonify({"success": False, "message": "Supabase credentials not configured on the server"}), 500
        
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Read file content
    file_bytes = file.read()
    
    # Generate unique filename
    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    
    try:
        # Upload
        res = supabase.storage.from_("experience-files").upload(
            file=file_bytes,
            path=unique_filename,
            file_options={"content-type": file.content_type}
        )
        
        # Get public url
        public_url = supabase.storage.from_("experience-files").get_public_url(unique_filename)
        
        # Update db
        experience.file_url = public_url
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "File uploaded successfully",
            "data": experience.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"File upload failed: {str(e)}"
        }), 500

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

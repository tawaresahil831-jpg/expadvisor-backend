import os
from flask import Flask, jsonify
from flask_cors import CORS
from app.config import Config
from app.extensions import db, limiter

def basedir_instance():
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(os.path.join(basedir_instance(), "instance"), exist_ok=True)

    db.init_app(app)
    limiter.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from app.models import User, Experience, Comment, Like

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.user import user_bp
    app.register_blueprint(user_bp)

    from app.routes.experience import experience_bp
    app.register_blueprint(experience_bp)

    from app.routes.upload import upload_bp
    app.register_blueprint(upload_bp)

    from app.routes.comment import comment_bp
    app.register_blueprint(comment_bp)

    from app.routes.like import like_bp
    app.register_blueprint(like_bp)

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    @app.route("/api/health")
    def health_check():
        return jsonify({
            "success": True,
            "message": "ExpAdvisor backend is running"
        }), 200

    
    from .routes.notification import notification_bp
    app.register_blueprint(notification_bp)
    
    return app

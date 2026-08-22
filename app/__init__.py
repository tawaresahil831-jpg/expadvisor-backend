import os
from flask import Flask, jsonify
from app.config import Config
from app.extensions import db

def basedir_instance():
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(os.path.join(basedir_instance(), "instance"), exist_ok=True)

    db.init_app(app)

    from app.models import User, Experience, Comment, Like

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.experience import experience_bp
    app.register_blueprint(experience_bp)

    from app.routes.comment import comment_bp
    app.register_blueprint(comment_bp)

    from app.routes.like import like_bp
    app.register_blueprint(like_bp)

    @app.route("/api/health")
    def health_check():
        return jsonify({
            "success": True,
            "message": "ExpAdvisor backend is running"
        }), 200

    return app

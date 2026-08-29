from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    college = db.Column(db.String(150))
    branch = db.Column(db.String(100))
    year = db.Column(db.Integer)
    role = db.Column(db.String(20), nullable=False, default="student")
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(300), nullable=True)
    github = db.Column(db.String(255), nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)
    portfolio = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    def set_password(self, plain_password):
        """Hashes and stores the password. Never save plain text."""
        self.password_hash = generate_password_hash(plain_password, method="pbkdf2:sha256")

    def check_password(self, plain_password):
        """Compares a plain password against the stored hash."""
        return check_password_hash(self.password_hash, plain_password)

    def to_dict(self):
        """Safe dict for API responses — password_hash is deliberately excluded."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "college": self.college,
            "branch": self.branch,
            "year": self.year,
            "role": self.role,
            "bio": self.bio,
            "skills": self.skills,
            "avatar_url": self.avatar_url,
            "github": self.github,
            "linkedin": self.linkedin,
            "portfolio": self.portfolio,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

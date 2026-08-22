from datetime import datetime
from app.extensions import db


class Comment(db.Model):
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(db.Integer, db.ForeignKey("experiences.experience_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="comments")
    experience = db.relationship("Experience", backref="comments")

    def to_dict(self):
        return {
            "comment_id": self.comment_id,
            "experience_id": self.experience_id,
            "user_id": self.user_id,
            "user_name": self.user.name if self.user else None,
            "comment": self.comment,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

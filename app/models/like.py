from datetime import datetime
from app.extensions import db


class Like(db.Model):
    __tablename__ = "likes"

    like_id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(db.Integer, db.ForeignKey("experiences.experience_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="likes")
    experience = db.relationship("Experience", backref="likes")

    __table_args__ = (
        db.UniqueConstraint("experience_id", "user_id", name="unique_like_per_user"),
    )

    def to_dict(self):
        return {
            "like_id": self.like_id,
            "experience_id": self.experience_id,
            "user_id": self.user_id,
            "user_name": self.user.name if self.user else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
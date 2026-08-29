from datetime import datetime
from app.extensions import db


class Experience(db.Model):
    __tablename__ = "experiences"

    experience_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    company = db.Column(db.String(150))
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    semester = db.Column(db.String(20))
    tags = db.Column(db.String(255))
    file_url = db.Column(db.String(300))
    views = db.Column(db.Integer, default=0)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = db.relationship("User", backref="experiences")

    def to_dict(self):
        accepted_answer = None
        for c in self.comments:
            if getattr(c, 'is_accepted', False):
                accepted_answer = c.comment
                break

        return {
            "accepted_answer": accepted_answer,
            "experience_id": self.experience_id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "company": self.company,
            "author_id": self.author_id,
            "author_name": self.author.name if self.author else None,
            "semester": self.semester,
            "tags": self.tags,
            "file_url": self.file_url,
            "views": self.views or 0,
            "is_resolved": self.is_resolved or False,
            "likes_count": len(self.likes) if hasattr(self, 'likes') and self.likes else 0,
            "comments_count": len(self.comments) if hasattr(self, 'comments') and self.comments else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

from app.extensions import db
from datetime import datetime

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    experience_id = db.Column(db.Integer, db.ForeignKey('experiences.experience_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure one bookmark per user per experience
    __table_args__ = (
        db.UniqueConstraint('user_id', 'experience_id', name='uq_user_experience_bookmark'),
    )
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    experience = db.relationship('Experience', foreign_keys=[experience_id])
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "experience_id": self.experience_id,
            "experience": self.experience.to_dict() if self.experience else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

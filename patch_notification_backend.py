import os
import sys

sys.path.insert(0, '/Users/sahiltaware415/expadvisor-backend')

from app import create_app
from app.extensions import db
from sqlalchemy import text

# 1. Update app/models/notification.py
model_code = """from app.extensions import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    experience_id = db.Column(db.Integer, db.ForeignKey('experiences.experience_id'), nullable=True)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    actor = db.relationship('User', foreign_keys=[actor_id])
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "actor_id": self.actor_id,
            "actor_name": self.actor.name if self.actor else None,
            "actor_avatar": self.actor.avatar_url if self.actor else None,
            "experience_id": self.experience_id,
            "message": self.message,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
"""
with open('/Users/sahiltaware415/expadvisor-backend/app/models/notification.py', 'w') as f:
    f.write(model_code)

# 3. Create table using raw SQL
app = create_app()
with app.app_context():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS notifications (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
        actor_id INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
        experience_id INTEGER REFERENCES experiences(experience_id) ON DELETE CASCADE,
        message VARCHAR(255) NOT NULL,
        is_read BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        db.session.execute(text(create_table_sql))
        db.session.commit()
        print("Successfully created notifications table.")
    except Exception as e:
        print(f"Error creating table: {e}")
        db.session.rollback()


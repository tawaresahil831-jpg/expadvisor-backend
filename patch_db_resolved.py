import os
import sys

sys.path.insert(0, '/Users/sahiltaware415/expadvisor-backend')

from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    # Add columns using SQL
    try:
        db.session.execute(text("ALTER TABLE experiences ADD COLUMN is_resolved BOOLEAN DEFAULT FALSE;"))
        print("Added is_resolved to experiences.")
    except Exception as e:
        print("Could not add is_resolved (maybe already exists):", e)
        db.session.rollback()

    try:
        db.session.execute(text("ALTER TABLE comments ADD COLUMN is_accepted BOOLEAN DEFAULT FALSE;"))
        print("Added is_accepted to comments.")
    except Exception as e:
        print("Could not add is_accepted (maybe already exists):", e)
        db.session.rollback()
        
    db.session.commit()
    print("Database columns migrated successfully.")

# Update Models
exp_model = '/Users/sahiltaware415/expadvisor-backend/app/models/experience.py'
with open(exp_model, 'r') as f:
    content = f.read()
if 'is_resolved = db.Column(db.Boolean' not in content:
    content = content.replace('views = db.Column(db.Integer, default=0)', 'views = db.Column(db.Integer, default=0)\n    is_resolved = db.Column(db.Boolean, default=False)')
    content = content.replace('"views": self.views,', '"views": self.views,\n            "is_resolved": self.is_resolved,')
    with open(exp_model, 'w') as f:
        f.write(content)

comment_model = '/Users/sahiltaware415/expadvisor-backend/app/models/comment.py'
with open(comment_model, 'r') as f:
    content = f.read()
if 'is_accepted = db.Column(db.Boolean' not in content:
    content = content.replace('created_at = db.Column(db.DateTime, default=datetime.utcnow)', 'created_at = db.Column(db.DateTime, default=datetime.utcnow)\n    is_accepted = db.Column(db.Boolean, default=False)')
    content = content.replace('"created_at": self.created_at.isoformat() if self.created_at else None', '"created_at": self.created_at.isoformat() if self.created_at else None,\n            "is_accepted": self.is_accepted')
    with open(comment_model, 'w') as f:
        f.write(content)

print("Models patched successfully.")

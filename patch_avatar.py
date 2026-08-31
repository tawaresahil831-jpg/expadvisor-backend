import sys
import os

sys.path.insert(0, '/Users/sahiltaware415/expadvisor-backend')

from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE users ADD COLUMN avatar_url VARCHAR(300);"))
        print("Successfully added avatar_url column.")
    except Exception as e:
        print(f"avatar_url column might already exist or error: {e}")
        db.session.rollback()
        
    db.session.commit()
    print("Migration complete.")

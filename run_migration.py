import sys
import os

# Add the backend dir to the path so we can import app
sys.path.insert(0, '/Users/sahiltaware415/expadvisor-backend')

from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Add bio column
        db.session.execute(text("ALTER TABLE users ADD COLUMN bio TEXT;"))
        print("Successfully added bio column.")
    except Exception as e:
        print(f"Bio column might already exist or error: {e}")
        db.session.rollback()

    try:
        # Add skills column
        db.session.execute(text("ALTER TABLE users ADD COLUMN skills TEXT;"))
        print("Successfully added skills column.")
    except Exception as e:
        print(f"Skills column might already exist or error: {e}")
        db.session.rollback()
        
    db.session.commit()
    print("Migration complete.")

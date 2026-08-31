import sys
sys.path.insert(0, '/Users/sahiltaware415/expadvisor-backend')
# pyrefly: ignore [missing-import]
from app import create_app
from app.extensions import db
from app.models.experience import Experience

app = create_app()
with app.app_context():
    exps = Experience.query.all()
    print(f"Total experiences in DB: {len(exps)}")
    for e in exps:
        print(f"- {e.title}")

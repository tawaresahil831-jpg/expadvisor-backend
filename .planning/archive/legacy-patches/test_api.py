import sys
import json
sys.path.insert(0, '/Users/sahiltaware415/expadvisor-backend')
from app import create_app
from app.extensions import db
from app.models.experience import Experience

app = create_app()
with app.app_context():
    exps = Experience.query.all()
    print(json.dumps([e.to_dict() for e in exps], indent=2))

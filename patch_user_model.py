filepath = '/Users/sahiltaware415/expadvisor-backend/app/models/user.py'
with open(filepath, 'r') as f:
    content = f.read()

target = """    year = db.Column(db.Integer)
    role = db.Column(db.String(20), nullable=False, default="student")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)"""

replacement = """    year = db.Column(db.Integer)
    role = db.Column(db.String(20), nullable=False, default="student")
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)"""

content = content.replace(target, replacement)

target2 = """            "year": self.year,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }"""

replacement2 = """            "year": self.year,
            "role": self.role,
            "bio": self.bio,
            "skills": self.skills,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }"""

content = content.replace(target2, replacement2)

with open(filepath, 'w') as f:
    f.write(content)
print("Done")

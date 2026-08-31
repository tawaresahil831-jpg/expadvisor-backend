with open('/Users/sahiltaware415/expadvisor-backend/app/models/experience.py', 'r') as f:
    content = f.read()

# Add the views column
if 'views = db.Column' not in content:
    content = content.replace(
        'created_at = db.Column(db.DateTime, default=datetime.utcnow)',
        'views = db.Column(db.Integer, default=0)\n    created_at = db.Column(db.DateTime, default=datetime.utcnow)'
    )

# Add to to_dict
if '"views": self.views' not in content:
    content = content.replace(
        '"file_url": self.file_url,',
        '"file_url": self.file_url,\n            "views": self.views,'
    )

with open('/Users/sahiltaware415/expadvisor-backend/app/models/experience.py', 'w') as f:
    f.write(content)
print("Experience model patched successfully.")

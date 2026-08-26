import re

filepath = '/Users/sahiltaware415/expadvisor-backend/app/models/user.py'
with open(filepath, 'r') as f:
    content = f.read()

# Add avatar_url column
if 'avatar_url = db.Column' not in content:
    content = content.replace(
        'skills = db.Column(db.Text, nullable=True)',
        'skills = db.Column(db.Text, nullable=True)\n    avatar_url = db.Column(db.String(300), nullable=True)'
    )

# Add avatar_url to to_dict
if '"avatar_url": self.avatar_url' not in content:
    content = content.replace(
        '"skills": self.skills,',
        '"skills": self.skills,\n            "avatar_url": self.avatar_url,'
    )

with open(filepath, 'w') as f:
    f.write(content)

print("Patched app/models/user.py")

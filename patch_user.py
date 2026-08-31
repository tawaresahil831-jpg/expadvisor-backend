with open("app/models/user.py", "r") as f:
    content = f.read()

target = 'role = db.Column(db.String(20), nullable=False, default="student")\n    created_at = db.Column(db.DateTime, default=datetime.utcnow)'
replacement = target + '\n    reset_token = db.Column(db.String(100), unique=True, nullable=True)\n    reset_token_expiry = db.Column(db.DateTime, nullable=True)'

if target in content and "reset_token =" not in content:
    with open("app/models/user.py", "w") as f:
        f.write(content.replace(target, replacement))
    print("Patched user.py")
else:
    print("Could not find target or already patched.")

filepath = '/Users/sahiltaware415/expadvisor-backend/app/__init__.py'
with open(filepath, 'r') as f:
    content = f.read()

target = """    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)"""

replacement = """    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.user import user_bp
    app.register_blueprint(user_bp)"""

if "from app.routes.user import user_bp" not in content:
    content = content.replace(target, replacement)
    with open(filepath, 'w') as f:
        f.write(content)
print("Done patching __init__.py")

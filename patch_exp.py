filepath = '/Users/sahiltaware415/expadvisor-backend/app/routes/experience.py'
with open(filepath, 'r') as f:
    content = f.read()

target = """    category = request.args.get("category")
    company = request.args.get("company")
    search = request.args.get("search")

    query = Experience.query

    if category:"""

replacement = """    category = request.args.get("category")
    company = request.args.get("company")
    search = request.args.get("search")
    author_id = request.args.get("author_id")

    query = Experience.query

    if author_id:
        try:
            query = query.filter(Experience.author_id == int(author_id))
        except ValueError:
            pass

    if category:"""

content = content.replace(target, replacement)
with open(filepath, 'w') as f:
    f.write(content)
print("Done patching experience.py")

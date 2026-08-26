with open("run.py", "r") as f:
    content = f.read()

new_content = content.replace("app.run(debug=True)", "app.run(debug=True, port=5001)")

with open("run.py", "w") as f:
    f.write(new_content)

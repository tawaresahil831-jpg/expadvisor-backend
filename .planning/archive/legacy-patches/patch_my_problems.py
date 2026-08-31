import re

filepath = 'my_problems.html'
with open(filepath, 'r') as f:
    content = f.read()

# Replace tabs text with ID spans
content = content.replace(
    'Asked (4)',
    '<span id="asked-count">Asked (0)</span>'
)
content = content.replace(
    'Solved (12)',
    '<span id="solved-count">Solved (0)</span>'
)

# Fix Javascript to update tab counts
js_old = "if (askedList.length === 0) {"
js_new = """
            document.getElementById('asked-count').textContent = `Asked (${askedList.length})`;
            document.getElementById('solved-count').textContent = `Solved (${solvedList.length})`;
            
            if (askedList.length === 0) {"""
content = content.replace(js_old, js_new)

# Fix Sidebar Student label
content = content.replace(
    '<p class="text-label-sm font-label-sm text-on-surface-variant uppercase tracking-wider">Student</p>',
    '<p class="text-label-sm font-label-sm text-on-surface-variant uppercase tracking-wider user-role-display">Student</p>'
)

# Fix Spring 2024
content = content.replace(
    '<p class="text-label-md font-label-md text-primary">Spring 2024</p>',
    '<p class="text-label-md font-label-md text-primary">2026-2027</p>'
)

with open(filepath, 'w') as f:
    f.write(content)

print("Done patching my_problems.html")

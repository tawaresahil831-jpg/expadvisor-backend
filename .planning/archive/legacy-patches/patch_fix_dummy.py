import re

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/dashboard.html'
with open(filepath, 'r') as f:
    content = f.read()

# I want to delete everything between:
# <div id="feedContainer" class="flex flex-col gap-6">
# AND
# <!-- Pagination -->
start_str = '<div id="feedContainer" class="flex flex-col gap-6">'
end_str = '<!-- Pagination -->'
start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + start_str + '\n                            <!-- Experiences will be dynamically loaded here by JavaScript -->\n                        </div>\n\n                        ' + content[end_idx:]
    with open(filepath, 'w') as f:
        f.write(new_content)
    print("Fixed dummy html properly.")
else:
    print("Could not find start or end strings.")

import re

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/dashboard.html'
with open(filepath, 'r') as f:
    content = f.read()

# Find feedContainer start and its closing div
start_idx = content.find('<div id="feedContainer" class="flex flex-col gap-6">')
if start_idx != -1:
    # Find the next </div> that closes feedContainer, wait no, there's multiple nested divs.
    # It's easier to just regex the articles away inside it, OR we know the last dummy article is before "<!-- Pagination -->"
    end_idx = content.find('<!-- Pagination -->', start_idx)
    if end_idx != -1:
        new_content = content[:start_idx] + '<div id="feedContainer" class="flex flex-col gap-6">\n                            <!-- Experiences will be dynamically loaded here by JavaScript -->\n                        </div>\n                        ' + content[end_idx:]
        with open(filepath, 'w') as f:
            f.write(new_content)
        print("Removed dummy feed articles.")

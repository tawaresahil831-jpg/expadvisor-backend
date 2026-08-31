import re

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/dashboard.html'
with open(filepath, 'r') as f:
    content = f.read()

# The feedContainer now looks like:
# <div id="feedContainer" class="flex flex-col gap-6">
#                             <!-- Experiences will be dynamically loaded here by JavaScript -->
#                         </div>

start_search = '<div id="feedContainer" class="flex flex-col gap-6">\n                            <!-- Experiences will be dynamically loaded here by JavaScript -->\n                        </div>'
start_idx = content.find(start_search)
if start_idx != -1:
    end_idx = content.find('<!-- ---- Load More ---- -->', start_idx)
    if end_idx != -1:
        new_content = content[:start_idx + len(start_search)] + '\n\n                        ' + content[end_idx:]
        with open(filepath, 'w') as f:
            f.write(new_content)
        print("Cleaned up orphaned dummy articles.")
    else:
        print("Could not find Load More")
else:
    print("Could not find feedContainer")

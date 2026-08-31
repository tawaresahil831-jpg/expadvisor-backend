import re

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/dashboard.html'
with open(filepath, 'r') as f:
    content = f.read()

old_logic = """        // If it's not a category, just use the search filter
        if (!matched) {
            // Deselect all categories
            catBtns.forEach(b => {
                b.classList.remove('bg-secondary', 'text-on-secondary', 'shadow-sm');
                b.classList.add('bg-surface', 'text-on-surface-variant', 'border', 'border-outline-variant/30');
            });
            currentCategory = '';
            loadExperiences();
        }"""

new_logic = """        // If it's not a category, just use the search filter
        if (!matched) {
            // Deselect all categories
            catBtns.forEach(b => {
                b.classList.remove('bg-secondary', 'text-on-secondary', 'shadow-sm');
                b.classList.add('bg-surface-container-high', 'text-on-surface-variant', 'hover:bg-surface-container-highest');
            });
            currentCategory = '';
        }
        currentPage = 1;
        loadExperiences();"""

content = content.replace(old_logic, new_logic)

with open(filepath, 'w') as f:
    f.write(content)

print("Hashtag logic patched.")

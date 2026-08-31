import re
import os

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/dashboard.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add filter-cat-btn to category buttons
# They look like: <button class="px-4 py-1.5 rounded-full bg-secondary text-on-secondary font-label-sm">All</button>
content = content.replace('font-label-sm">All</button>', 'font-label-sm filter-cat-btn">All</button>')
content = content.replace('font-label-sm hover:bg-surface-container-highest">Tech</button>', 'font-label-sm hover:bg-surface-container-highest filter-cat-btn">Tech</button>')
content = content.replace('font-label-sm hover:bg-surface-container-highest">Career</button>', 'font-label-sm hover:bg-surface-container-highest filter-cat-btn">Career</button>')
content = content.replace('font-label-sm hover:bg-surface-container-highest">Design</button>', 'font-label-sm hover:bg-surface-container-highest filter-cat-btn">Design</button>')

# 2. Add hashtag formatting logic
hashtag_logic = """
    function formatHashtags(text) {
        if (!text) return '';
        // Escape HTML to prevent XSS before parsing hashtags
        const escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
        return escaped.replace(/#(\w+)/g, '<span class="text-secondary font-semibold hover:underline cursor-pointer" onclick="event.stopPropagation(); setHashtagSearch(\\'$1\\')">#$1</span>');
    }

    function setHashtagSearch(tag) {
        currentSearch = tag;
        const searchInput = document.getElementById('searchInput');
        if (searchInput) searchInput.value = currentSearch;
        
        // Also try to match a category button if it's an exact match
        const catBtns = document.querySelectorAll('.filter-cat-btn');
        let matched = false;
        catBtns.forEach(b => {
            if (b.textContent.trim().toLowerCase() === tag.toLowerCase()) {
                b.click(); // This will trigger the category filter
                matched = true;
            }
        });
        
        // If it's not a category, just use the search filter
        if (!matched) {
            // Deselect all categories
            catBtns.forEach(b => {
                b.classList.remove('bg-secondary', 'text-on-secondary', 'shadow-sm');
                b.classList.add('bg-surface', 'text-on-surface-variant', 'border', 'border-outline-variant/30');
            });
            currentCategory = '';
            loadExperiences();
        }
    }
"""

# Insert hashtag_logic somewhere inside the script tag
insert_idx = content.find("async function loadExperiences()")
content = content[:insert_idx] + hashtag_logic + "\n    " + content[insert_idx:]

# 3. Update loadExperiences rendering
content = content.replace('>${exp.title}</h3>', '>${formatHashtags(exp.title)}</h3>')
content = content.replace('>${exp.content}</p>', '>${formatHashtags(exp.content)}</p>')

# 4. Update openExperienceDetail rendering
content = content.replace("document.getElementById('detailTitle').textContent = exp.title;", "document.getElementById('detailTitle').innerHTML = formatHashtags(exp.title);")
content = content.replace("document.getElementById('detailDescription').textContent = exp.content;", "document.getElementById('detailDescription').innerHTML = formatHashtags(exp.content);")

with open(filepath, 'w') as f:
    f.write(content)

print("Added category button functionality and hashtag parsing to dashboard.html")

import re
import os

files = ['dashboard.html', 'my_profile.html', 'solve.html']

role_block = """
            <div class="px-4 py-2 mt-4 mb-1">
                <p class="text-label-sm font-label-sm text-on-surface-variant uppercase tracking-wider user-role-display">Student</p>
            </div>
"""

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check if it already has the block (some variant of it)
        if 'user-role-display' in content.split('<nav')[1].split('</nav>')[0]:
            print(f"Role display already exists in sidebar of {filepath}")
            continue
            
        # Add it right after <nav ...>
        # Let's find <nav class="flex-1 px-4 flex flex-col gap-1">
        
        nav_pattern = r'(<nav[^>]*>)'
        content = re.sub(nav_pattern, r'\1' + role_block, content, count=1)
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched sidebar for {filepath}")


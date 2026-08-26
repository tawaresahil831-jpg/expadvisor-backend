import re
import os

files = ['dashboard.html', 'my_problems.html']

profile_btn = """
            <a class="flex items-center px-4 py-3 rounded-xl text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-all font-label-md text-label-md" href="my_profile.html">
                <span class="material-symbols-outlined mr-3">person</span>My Profile
            </a>"""

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the "My Problems" button and insert "My Profile" after it
    # We can just look for `assignment</span>My Problems\n            </a>`
    pattern = r'(<span class="material-symbols-outlined mr-3">assignment</span>My Problems\s*</a>)'
    
    if 'href="my_profile.html"' not in content:
        content = re.sub(pattern, r'\1' + profile_btn, content)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")
    else:
        print(f"{filepath} already has My Profile")


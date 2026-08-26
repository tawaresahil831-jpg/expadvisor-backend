import re
import os

files = ['dashboard.html', 'my_problems.html', 'my_profile.html']

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        # 1. Add user-role-display to the header role
        # We know it comes right after user-name-display
        content = re.sub(
            r'(<p class="[^"]*user-name-display[^"]*">[^<]*</p>\s*)<p class="([^"]*)">([^<]*)</p>',
            r'\1<p class="\2 user-role-display">\3</p>',
            content
        )
        
        # 2. Remove the Solve Queue link from sidebar
        solve_link_pattern = r'<a class="[^"]*" href="solve\.html">\s*<span class="[^"]*">queue_play_next</span>Solve Queue\s*</a>'
        content = re.sub(solve_link_pattern, '', content)
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filepath}")


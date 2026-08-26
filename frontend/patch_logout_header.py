import re
import os

files = ['dashboard.html', 'my_problems.html', 'my_profile.html']

logout_btn = """
            <a class="flex items-center px-4 py-3 rounded-xl text-error hover:bg-error/10 hover:text-error transition-all font-label-md text-label-md mt-auto" href="#" onclick="logout(); return false;">
                <span class="material-symbols-outlined text-[20px] mr-3">logout</span>
                Logout
            </a>
"""

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()

        # 1. Add logout button to sidebar if not present
        if 'onclick="logout(); return false;"' not in content:
            # Find the end of <nav ...> ... </nav>
            # The last element inside nav is usually My Profile
            # Let's just insert it right before </nav>
            content = re.sub(r'(</nav>)', logout_btn + r'\1', content)

        # 2. Fix the header right side
        # The user wants ONLY the profile photo and the user's name
        # Let's remove the user-role-display <p>
        role_pattern = r'<p class="[^"]*user-role-display[^"]*">[^<]*</p>'
        content = re.sub(role_pattern, '', content)

        # Remove the "My Profile" button
        profile_btn_pattern = r'<a class="[^"]*" href="my_profile\.html">\s*<span class="[^"]*">person</span>My Profile\s*</a>'
        content = re.sub(profile_btn_pattern, '', content)
        
        # Also, since we removed the "My Profile" button, we might want to make the profile picture / name clickable to go to the profile page?
        # The user didn't ask for it, but usually, headers have clickable profiles. Let's wrap the name+image in an <a> tag pointing to my_profile.html.
        # Actually, let's just do exactly what they asked to be safe.
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filepath}")


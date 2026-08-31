import re
import os

files = ['my_problems.html', 'my_profile.html']
dashboard_path = 'dashboard.html'

# 1. Extract header from dashboard
with open(dashboard_path, 'r') as f:
    dashboard_content = f.read()

header_match = re.search(r'(<header class="fixed top-0 left-72 right-0 h-16 bg-surface/80.*?</header>)', dashboard_content, re.DOTALL)
if not header_match:
    print("Could not find header in dashboard.html")
    exit(1)

header_html = header_match.group(1)

# 2. Sync header to other files
for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Replace header
        content = re.sub(r'<header class="fixed top-0 left-72 right-0 h-16 bg-surface/80.*?</header>', header_html, content, flags=re.DOTALL)
        
        # Remove Administrative section from my_problems
        if filepath == 'my_problems.html':
            admin_block = r'<div class="px-4 py-2 mt-6 mb-1 border-t border-outline-variant/20 pt-6">\s*<p class="text-label-sm font-label-sm text-on-surface-variant uppercase tracking-wider">Administrative</p>\s*</div>\s*<a class="flex items-center px-4 py-3 rounded-xl text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-all font-label-md text-label-md" href="#">\s*<span class="material-symbols-outlined mr-3">admin_panel_settings</span>Admin Dashboard\s*</a>'
            content = re.sub(admin_block, '', content)
            
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Synced {filepath}")

# 3. Append global UI logic to api.js so the dropdown works everywhere
with open('js/api.js', 'a') as f:
    f.write("""
// Global UI Bindings
document.addEventListener('DOMContentLoaded', () => {
    // Notification Dropdown Logic
    const notifBtn = document.getElementById('notificationBtn');
    const notifDropdown = document.getElementById('notificationDropdown');
    if (notifBtn && notifDropdown) {
        // Prevent multiple bindings if already bound elsewhere
        if (!notifBtn.dataset.bound) {
            notifBtn.dataset.bound = 'true';
            notifBtn.addEventListener('click', (e) => {
                notifDropdown.classList.toggle('hidden');
                e.stopPropagation();
            });
            document.addEventListener('click', (e) => {
                if (!notifDropdown.contains(e.target) && e.target !== notifBtn) {
                    notifDropdown.classList.add('hidden');
                }
            });
        }
    }
});
""")
print("Added global UI logic to api.js")

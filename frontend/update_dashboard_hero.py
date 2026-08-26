import re

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/dashboard.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Replace Hero Buttons with Trending Topic Widget
old_hero_buttons = r'<div class="z-10 relative flex gap-4">\s*<button onclick="document\.getElementById\(\'createModal\'\)\.showModal\(\)".*?</button>\s*<button onclick="window\.location\.href=\'solve\.html\'".*?</button>\s*</div>'

trending_widget = """<div class="z-10 relative bg-surface-container-high rounded-xl p-4 shadow-sm border border-outline-variant/20 max-w-sm ml-auto animate-fade-in-up">
                        <div class="flex items-center justify-between mb-2">
                            <div class="flex items-center gap-2 text-error">
                                <span class="material-symbols-outlined text-[18px]">local_fire_department</span>
                                <span class="font-label-md text-label-sm font-bold uppercase tracking-wider">Trending Now</span>
                            </div>
                            <span class="px-2 py-0.5 rounded bg-primary/10 text-primary text-[10px] font-bold uppercase">Web Dev</span>
                        </div>
                        <h3 class="font-headline-sm text-headline-sm text-on-surface mb-3">How to optimize React rendering performance?</h3>
                        <div class="flex items-center justify-between">
                            <div class="flex -space-x-2">
                                <img src="https://i.pravatar.cc/100?img=1" class="w-6 h-6 rounded-full border-2 border-surface">
                                <img src="https://i.pravatar.cc/100?img=2" class="w-6 h-6 rounded-full border-2 border-surface">
                                <img src="https://i.pravatar.cc/100?img=3" class="w-6 h-6 rounded-full border-2 border-surface">
                            </div>
                            <button class="text-primary font-label-md text-label-sm hover:underline flex items-center gap-1">
                                Join Discussion <span class="material-symbols-outlined text-[14px]">arrow_forward</span>
                            </button>
                        </div>
                    </div>"""

content = re.sub(old_hero_buttons, trending_widget, content, flags=re.DOTALL)

# 2. Add a "Create Post" button to the sidebar
# Find the start of <nav class="flex flex-col gap-2 mt-8 flex-1">
sidebar_nav = r'<nav class="flex flex-col gap-2 mt-8 flex-1">'
create_btn = """<nav class="flex flex-col gap-2 mt-8 flex-1">
            <button onclick="document.getElementById('createModal').showModal()" class="flex items-center justify-center gap-2 w-full bg-primary text-on-primary px-4 py-3 rounded-xl shadow-sm hover:bg-inverse-surface transition-colors font-label-md text-label-md mb-4">
                <span class="material-symbols-outlined">add_circle</span>
                New Post
            </button>"""

content = content.replace('<nav class="flex flex-col gap-2 mt-8 flex-1">', create_btn)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated dashboard.html with Trending widget and New Post sidebar button.")

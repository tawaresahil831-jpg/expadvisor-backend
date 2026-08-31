import re

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/dashboard.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Update the status filtering in loadExperiences
# currentStatus === 'Open' -> !e.is_resolved
# currentStatus === 'Answered' -> e.is_resolved
filter_old = """
            if (currentStatus === 'Open') {
                expList = expList.filter(e => e.comments_count === 0);
            } else if (currentStatus === 'Answered') {
                expList = expList.filter(e => e.comments_count > 0);
            }
"""
filter_new = """
            if (currentStatus === 'Open') {
                expList = expList.filter(e => !e.is_resolved);
            } else if (currentStatus === 'Answered') {
                expList = expList.filter(e => e.is_resolved);
            }
"""
content = content.replace(filter_old, filter_new)

# 2. Add Resolved badge to the feed cards
badge_feed_old = """
                        <div class="flex items-center gap-2 mb-2 text-label-sm text-on-surface-variant font-label-sm">
                            <span class="px-2 py-0.5 rounded-md bg-secondary/10 text-secondary">${exp.category || 'General'}</span>
                            <span>•</span>
"""
badge_feed_new = """
                        <div class="flex items-center gap-2 mb-2 text-label-sm text-on-surface-variant font-label-sm">
                            <span class="px-2 py-0.5 rounded-md bg-secondary/10 text-secondary">${exp.category || 'General'}</span>
                            ${exp.is_resolved ? `<span class="px-2 py-0.5 rounded-md bg-[#22c55e]/15 text-[#16a34a] flex items-center gap-1 font-semibold"><span class="material-symbols-outlined text-[14px]">check_circle</span>Resolved</span>` : ''}
                            <span>•</span>
"""
content = content.replace(badge_feed_old, badge_feed_new)

with open(filepath, 'w') as f:
    f.write(content)

print("Patched dashboard.html feed UI")

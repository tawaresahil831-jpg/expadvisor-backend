import re

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/dashboard.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Update renderComments signature and call
content = content.replace('function renderComments(comments) {', 'function renderComments(comments, authorId) {')
content = content.replace('renderComments(comments);', 'renderComments(comments, exp.author_id);')

# 2. Update renderComments map logic
render_logic_old = """
        container.innerHTML = comments.map(c => `
            <div class="bg-surface-container-low p-4 rounded-xl border border-outline-variant/20">
                <div class="flex justify-between items-center mb-1">
"""
render_logic_new = """
        container.innerHTML = comments.map(c => `
            <div class="p-4 rounded-xl border ${c.is_accepted ? 'bg-[#22c55e]/5 border-[#22c55e]/30' : 'bg-surface-container-low border-outline-variant/20'}">
                <div class="flex justify-between items-center mb-1">
"""
content = content.replace(render_logic_old, render_logic_new)

badge_logic_old = """
                    <span class="font-label-md text-on-surface" style="font-weight:600;">${c.user_name || 'User'}</span>
                    <div class="flex items-center gap-2">
"""
badge_logic_new = """
                    <div class="flex items-center gap-2">
                        <span class="font-label-md text-on-surface" style="font-weight:600;">${c.user_name || 'User'}</span>
                        ${c.is_accepted ? `<span class="px-2 py-0.5 rounded bg-[#22c55e] text-white flex items-center gap-1 font-semibold text-[10px]"><span class="material-symbols-outlined text-[12px]">check_circle</span>Accepted</span>` : ''}
                    </div>
                    <div class="flex items-center gap-2">
"""
content = content.replace(badge_logic_old, badge_logic_new)

btn_logic_old = """
                        ${(currentUserId && c.user_id === currentUserId) ? `
                            <button onclick="editComment(${c.comment_id}, \`${c.comment.replace(/`/g, "'")}\`)" class="text-secondary hover:text-primary transition-colors text-[14px]">
"""
btn_logic_new = """
                        ${(currentUserId === authorId && !c.is_accepted) ? `
                            <button onclick="acceptSolution(${c.comment_id})" class="text-[#22c55e] hover:text-[#16a34a] font-semibold text-[12px] bg-[#22c55e]/10 px-2 py-1 rounded transition-colors flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">check</span>Accept Solution</button>
                        ` : ''}
                        ${(currentUserId && c.user_id === currentUserId) ? `
                            <button onclick="editComment(${c.comment_id}, \`${c.comment.replace(/`/g, "'")}\`)" class="text-secondary hover:text-primary transition-colors text-[14px]">
"""
content = content.replace(btn_logic_old, btn_logic_new)


# 3. Add acceptSolution function
accept_func = """
    async function acceptSolution(commentId) {
        if (!confirm('Are you sure you want to accept this solution?')) return;
        const res = await apiRequest(`/comments/${commentId}/accept`, { method: 'PUT' });
        if (res.status === 200 && res.data.success) {
            openExperienceDetail(currentDetailExpId);
            loadExperiences();
        } else {
            alert(res.data.message || 'Failed to accept solution');
        }
    }
"""
insert_idx = content.find("function renderComments(")
content = content[:insert_idx] + accept_func + "\n    " + content[insert_idx:]

with open(filepath, 'w') as f:
    f.write(content)

print("Patched dashboard.html")

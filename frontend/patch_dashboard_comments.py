import re

filepath = 'dashboard.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Update populateUserProfile to save currentUserId
old_populate = "    populateUserProfile();"
new_populate = """    let currentUserId = null;
    populateUserProfile().then(u => {
        if (u) currentUserId = u.id || u.user_id;
    });"""
content = content.replace(old_populate, new_populate)

# 2. Update renderComments to add edit/delete and change time format
old_render_str = "    function renderComments(comments) {"
new_render_str = """
    async function deleteComment(id) {
        if (confirm("Are you sure you want to delete this comment?")) {
            const res = await apiRequest(`/comments/${id}`, { method: 'DELETE' });
            if (res.status === 200) {
                openExperienceDetail(currentDetailExpId);
            } else {
                alert('Failed to delete comment: ' + (res.data?.message || ''));
            }
        }
    }

    async function editComment(id, currentText) {
        const newText = prompt("Edit your comment:", currentText);
        if (newText !== null && newText.trim() !== currentText && newText.trim() !== "") {
            const res = await apiRequest(`/comments/${id}`, {
                method: 'PUT',
                body: { comment: newText.trim() }
            });
            if (res.status === 200) {
                openExperienceDetail(currentDetailExpId);
            } else {
                alert('Failed to edit comment: ' + (res.data?.message || ''));
            }
        }
    }

    function renderComments(comments) {"""
content = content.replace(old_render_str, new_render_str)

# Now update the inner HTML of the comment
old_comment_html = """            <div class="bg-surface-container-low p-4 rounded-xl border border-outline-variant/20">
                <div class="flex justify-between items-center mb-1">
                    <span class="font-label-md text-on-surface" style="font-weight:600;">${c.user_name || 'User'}</span>
                    <span class="text-[11px] text-on-surface-variant">${new Date(c.created_at).toLocaleDateString()}</span>
                </div>
                <p class="text-body-sm text-on-surface-variant">${c.comment}</p>
            </div>"""

new_comment_html = """            <div class="bg-surface-container-low p-4 rounded-xl border border-outline-variant/20">
                <div class="flex justify-between items-center mb-1">
                    <span class="font-label-md text-on-surface" style="font-weight:600;">${c.user_name || 'User'}</span>
                    <div class="flex items-center gap-2">
                        <span class="text-[11px] text-on-surface-variant">${new Date(c.created_at).toLocaleString([], {year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit'})}</span>
                        ${(currentUserId && c.user_id === currentUserId) ? `
                            <button onclick="editComment(${c.comment_id}, \`${c.comment.replace(/`/g, "'")}\`)" class="text-secondary hover:text-primary transition-colors text-[14px]">
                                <span class="material-symbols-outlined" style="font-size: 16px;">edit</span>
                            </button>
                            <button onclick="deleteComment(${c.comment_id})" class="text-error hover:text-error/80 transition-colors text-[14px]">
                                <span class="material-symbols-outlined" style="font-size: 16px;">delete</span>
                            </button>
                        ` : ''}
                    </div>
                </div>
                <p class="text-body-sm text-on-surface-variant">${c.comment}</p>
            </div>"""
content = content.replace(old_comment_html, new_comment_html)

with open(filepath, 'w') as f:
    f.write(content)

print("dashboard.html patched!")

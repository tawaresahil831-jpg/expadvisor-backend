import re

filepath = 'dashboard.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Update openExperienceDetail to fetch comments
old_fetch = r"renderComments\(exp\.comments \|\| \[\]\);"
new_fetch = """            // Fetch comments separately since they aren't included in the experience object
            const commentsRes = await apiRequest(`/experiences/${id}/comments`);
            let comments = [];
            if (commentsRes.status === 200 && commentsRes.data.success) {
                comments = commentsRes.data.data;
            }
            renderComments(comments);"""
content = re.sub(old_fetch, new_fetch, content)

# 2. Update renderComments to use correct fields (user_name, comment)
old_render = r"\$\{c\.author_name \|\| 'User'\}.*?\$\{new Date\(c\.created_at\)\.toLocaleDateString\(\)\}.*?\$\{c\.content\}"
new_render_string = "${c.user_name || 'User'}</span>\n                    <span class=\"text-[11px] text-on-surface-variant\">${new Date(c.created_at).toLocaleDateString()}</span>\n                </div>\n                <p class=\"text-body-sm text-on-surface-variant\">${c.comment}</p>"
# Let's just use string replace for renderComments
content = content.replace("${c.author_name || 'User'}", "${c.user_name || 'User'}")
content = content.replace("${c.content}", "${c.comment}")

with open(filepath, 'w') as f:
    f.write(content)

print("Comments fixed in dashboard.html")

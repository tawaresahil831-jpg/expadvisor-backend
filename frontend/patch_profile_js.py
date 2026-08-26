import re

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/my_profile.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Fix user_id bug
content = content.replace("currentUserId = userRes.data.data.id;", "currentUserId = userRes.data.data.user_id || userRes.data.data.id;")

# 2. Update motivational quote
old_quote = "Post experiences or leave comments to earn achievements!"
new_quote = "Every expert was once a beginner. Keep contributing to unlock achievements!"
content = content.replace(old_quote, new_quote)

# 3. Add uploadAvatar JS function
upload_js = """
    async function uploadAvatar(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        const formData = new FormData();
        formData.append('file', file);
        
        // Show uploading state
        const img = document.getElementById('profileAvatarImg');
        const oldSrc = img.src;
        img.style.opacity = '0.5';
        
        const res = await apiRequest('/users/me/avatar', {
            method: 'POST',
            body: formData,
            isFormData: true
        });
        
        img.style.opacity = '1';
        if (res.status === 200 && res.data.success) {
            const newUrl = res.data.data.avatar_url;
            img.src = newUrl;
            // Optionally update the header image too if we have one
        } else {
            alert('Failed to upload avatar: ' + (res.data?.message || ''));
            img.src = oldSrc;
        }
    }
"""
if 'function uploadAvatar' not in content:
    # Insert it before loadProfileData
    content = content.replace("async function loadProfileData() {", upload_js + "\n    async function loadProfileData() {")

# 4. Integrate Activity Graph real data
# Replace the static SVG generator with a dynamic one
static_svg_js = r"var svg = document\.getElementById\('contribution-graph'\);.*?svg\.innerHTML = content;"
dynamic_svg_js = """
    var svg = document.getElementById('contribution-graph');
    if (!svg) return;
    
    // Fetch real data
    // Note: since this runs in DOMContentLoaded, we need to wait for currentUserId.
    // Instead of doing it in DOMContentLoaded, we should do it inside loadProfileData.
"""
# So first, let's remove the DOMContentLoaded wrapper around the svg logic
# Actually, it's easier to just wipe the old script block entirely.

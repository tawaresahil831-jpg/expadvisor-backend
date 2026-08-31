import re

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/my_profile.html'
with open(filepath, 'r') as f:
    content = f.read()

# Remove old DOMContentLoaded script block
old_script_block = re.search(r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\', function\(\) \{\s*var svg = document\.getElementById\(\'contribution-graph\'\);.*?\}\);\s*</script>', content, re.DOTALL)
if old_script_block:
    content = content.replace(old_script_block.group(0), '')

# Now inject our new dynamic function and call it after currentUserId is found
new_js = """
    async function loadActivityGraph() {
        if (!currentUserId) return;
        var svg = document.getElementById('contribution-graph');
        if (!svg) return;
        
        const res = await apiRequest(`/users/${currentUserId}/activity`);
        let activityMap = {};
        if (res.status === 200 && res.data.success) {
            activityMap = res.data.data;
        }
        
        var cols = 52;
        var rows = 7;
        var cellSize = 11;
        var cellGap = 3;
        var intensityColors = [
            '#dce9ff', // 0 - lightest
            '#bcc7de', // 1
            '#8590a6', // 2
            '#545f73', // 3
            '#091426' // 4 - darkest
        ];
        
        // Build an array of the last 364 dates
        let dates = [];
        let today = new Date();
        for (let i = 363; i >= 0; i--) {
            let d = new Date(today);
            d.setDate(today.getDate() - i);
            dates.push(d.toISOString().split('T')[0]);
        }
        
        var contentHTML = '';
        let dateIndex = 0;
        for (var i = 0; i < cols; i++) {
            contentHTML += '<g transform="translate(' + (i * (cellSize + cellGap)) + ', 0)">';
            for (var j = 0; j < rows; j++) {
                if (dateIndex >= dates.length) break;
                let dateStr = dates[dateIndex++];
                let count = activityMap[dateStr] || 0;
                
                let intensity = 0;
                if (count > 0 && count <= 2) intensity = 1;
                else if (count > 2 && count <= 5) intensity = 2;
                else if (count > 5 && count <= 10) intensity = 3;
                else if (count > 10) intensity = 4;
                
                contentHTML += '<rect y="' + (j * (cellSize + cellGap)) + '" width="' + cellSize + '" height="' +
                    cellSize + '" rx="2" fill="' + intensityColors[intensity] +
                    '" class="hover:stroke-primary stroke-2 transition-all cursor-pointer" ' +
                    'title="' + count + ' contributions on ' + dateStr + '" />';
            }
            contentHTML += '</g>';
        }
        svg.innerHTML = contentHTML;
    }
"""

# Insert the function
content = content.replace("async function loadProfileData() {", new_js + "\n    async function loadProfileData() {")

# Call the function at the end of loadProfileData
content = content.replace("loadRecentActivity();", "loadRecentActivity();\n        loadActivityGraph();")

# Also, since we want to display the user's avatar from the DB:
# In loadProfileData, we should update the profile picture
avatar_update_logic = """
            if (data.avatar_url) {
                const img = document.getElementById('profileAvatarImg');
                if (img) img.src = data.avatar_url;
            }
"""
content = content.replace("document.getElementById('profile-bio').textContent = data.bio", "document.getElementById('profile-bio').textContent = data.bio" + avatar_update_logic)

with open(filepath, 'w') as f:
    f.write(content)

print("Activity graph and avatar loading patched!")

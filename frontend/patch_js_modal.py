import re

filepath = 'my_profile.html'
with open(filepath, 'r') as f:
    content = f.read()

modal_html = """
<!-- Edit Bio Modal -->
<div id="edit-bio-modal" class="hidden fixed inset-0 z-[100] flex items-center justify-center bg-scrim/40 backdrop-blur-sm p-4">
    <div class="bg-surface-container-high rounded-[28px] p-6 max-w-md w-full shadow-elevation-3 relative">
        <h3 class="font-headline-sm text-headline-sm text-on-surface mb-4">Edit Profile</h3>
        <div class="flex flex-col gap-4">
            <div class="flex flex-col gap-1.5">
                <label class="text-label-sm text-on-surface">Bio</label>
                <textarea id="edit-bio-input" class="w-full px-4 py-3 rounded-xl bg-surface border border-outline-variant/50 text-body-md text-on-surface placeholder:text-on-surface-variant/50 focus:outline-none focus:border-secondary focus:ring-2 focus:ring-secondary/50 transition-all min-h-[100px]" placeholder="Tell us about yourself..."></textarea>
            </div>
            <div class="flex justify-end gap-2 mt-4">
                <button type="button" id="close-bio-modal" class="px-6 py-2.5 rounded-full text-primary font-label-md hover:bg-primary/10 transition-colors">Cancel</button>
                <button type="button" id="save-bio-btn" class="px-6 py-2.5 rounded-full bg-primary text-on-primary font-label-md shadow-sm hover:shadow-md transition-shadow">Save</button>
            </div>
        </div>
    </div>
</div>
"""

new_script = """
<script>
    let currentUserId = null;

    async function loadProfileData() {
        const userRes = await apiRequest('/auth/me');
        if (userRes.status !== 200) {
            window.location.href = "login.html";
            return;
        }
        currentUserId = userRes.data.data.id;
        
        // Fetch full profile stats
        const profileRes = await apiRequest(`/users/${currentUserId}`);
        if (profileRes.status === 200 && profileRes.data.success) {
            const data = profileRes.data.data;
            document.getElementById('profile-name').textContent = data.name || 'Student';
            document.getElementById('profile-role').textContent = data.role ? data.role.toUpperCase() : 'STUDENT';
            document.getElementById('profile-bio').textContent = data.bio || 'Add a bio to let others know about your academic journey.';
            
            // Set Stats
            document.getElementById('stats-solved').textContent = data.stats.problems_solved || 0;
            document.getElementById('stats-helped').textContent = data.stats.peers_helped || 0;
            
            // Set Achievements
            const achievementsContainer = document.getElementById('achievements-container');
            if (data.achievements && data.achievements.length > 0) {
                achievementsContainer.innerHTML = data.achievements.map(ach => `
                    <div class="flex items-center gap-2 bg-surface-container-high rounded-xl p-2 pr-4 shadow-sm hover:-translate-y-1 transition-transform cursor-default">
                        <div class="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                            <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
                        </div>
                        <span class="font-label-md text-label-sm text-on-surface">${ach}</span>
                    </div>
                `).join('');
            } else {
                achievementsContainer.innerHTML = '<p class="text-on-surface-variant text-sm">Post experiences or leave comments to earn achievements!</p>';
            }
        }
        
        loadRecentActivity();
    }
    
    async function loadRecentActivity() {
        const container = document.getElementById('recent-activity-list');
        if (!container) return;
        
        if (!currentUserId) return;
        container.innerHTML = '<p class="text-center py-4 text-on-surface-variant">Loading recent activity...</p>';
        
        const response = await apiRequest(`/experiences?author_id=${currentUserId}`);
        if (response.status === 200 && response.data.success) {
            const myActivities = response.data.data.slice(0, 5); // Take top 5
            
            if (myActivities.length === 0) {
                container.innerHTML = '<p class="text-center py-4 text-on-surface-variant">No recent activity.</p>';
            } else {
                container.innerHTML = myActivities.map(exp => `
                    <div class="bg-surface rounded-xl p-4 flex items-center justify-between group hover:shadow-md transition-shadow">
                        <div class="flex items-center gap-4">
                            <div class="w-10 h-10 rounded-lg bg-primary-fixed text-on-primary-fixed flex items-center justify-center group-hover:scale-105 transition-transform">
                                <span class="material-symbols-outlined">forum</span>
                            </div>
                            <div>
                                <h4 class="font-headline-md text-body-lg text-on-surface line-clamp-1"><a href="dashboard.html">${exp.title}</a></h4>
                                <div class="flex items-center gap-3 mt-1">
                                    <span class="font-label-sm text-label-sm text-on-surface-variant bg-surface-container-high px-2 py-0.5 rounded-md">${exp.category || 'General'}</span>
                                    <span class="font-label-sm text-label-sm text-on-surface-variant flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">schedule</span>${new Date(exp.created_at).toLocaleDateString()}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('');
            }
        }
    }
    
    document.addEventListener('DOMContentLoaded', () => {
        loadProfileData();
        
        // Modal Logic
        const modal = document.getElementById('edit-bio-modal');
        const editBtn = document.getElementById('edit-bio-btn');
        const closeBtn = document.getElementById('close-bio-modal');
        const saveBtn = document.getElementById('save-bio-btn');
        const bioInput = document.getElementById('edit-bio-input');
        
        if (editBtn) {
            editBtn.addEventListener('click', () => {
                const currentBio = document.getElementById('profile-bio').textContent;
                bioInput.value = currentBio === 'Add a bio to let others know about your academic journey.' ? '' : currentBio;
                modal.classList.remove('hidden');
            });
        }
        
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.classList.add('hidden');
            });
        }
        
        if (saveBtn) {
            saveBtn.addEventListener('click', async () => {
                const newBio = bioInput.value;
                const origText = saveBtn.textContent;
                saveBtn.textContent = 'Saving...';
                saveBtn.disabled = true;
                
                const res = await apiRequest('/users/me', {
                    method: 'PUT',
                    body: { bio: newBio }
                });
                
                if (res.status === 200 && res.data.success) {
                    document.getElementById('profile-bio').textContent = res.data.data.bio || 'Add a bio to let others know about your academic journey.';
                    modal.classList.add('hidden');
                } else {
                    alert(res.data.message || 'Failed to update bio');
                }
                
                saveBtn.textContent = origText;
                saveBtn.disabled = false;
            });
        }
    });
</script>
"""

# Replace old script
content = re.sub(r'<script>\s*async function loadRecentSolutions\(\).*?loadRecentSolutions\);\s*</script>', new_script, content, flags=re.DOTALL)

# Inject modal just before </body>
content = content.replace('</body>', modal_html + '\n</body>')

with open(filepath, 'w') as f:
    f.write(content)

print("Done patching JS and Modal in my_profile.html")

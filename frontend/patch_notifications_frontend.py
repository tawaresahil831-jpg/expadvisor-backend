import os

api_js_path = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/js/api.js'

with open(api_js_path, 'r') as f:
    content = f.read()

if 'function loadNotifications' not in content:
    notif_logic = """

// Notification Logic
async function loadNotifications() {
    const res = await apiRequest('/notifications');
    if (res.status === 200 && res.data.success) {
        const notifications = res.data.data;
        
        // Find dropdowns in all headers (we use a specific ID, assuming there's only one header active)
        const dropdownContainer = document.querySelector('#notificationDropdown .max-h-64');
        const badge = document.querySelector('#notificationBtn span.bg-error');
        
        if (dropdownContainer) {
            if (notifications.length === 0) {
                dropdownContainer.innerHTML = '<div class="p-4 text-center text-on-surface-variant font-label-md">No new notifications</div>';
                if (badge) badge.style.display = 'none';
            } else {
                const unreadCount = notifications.filter(n => !n.is_read).length;
                if (badge) {
                    badge.style.display = unreadCount > 0 ? 'block' : 'none';
                }
                
                dropdownContainer.innerHTML = notifications.map(n => `
                    <div onclick="readNotification(${n.id})" class="p-4 border-b border-outline-variant/20 hover:bg-surface-container/50 transition-colors cursor-pointer flex gap-3 items-start ${n.is_read ? 'opacity-70' : ''}">
                        <div class="w-8 h-8 rounded-full bg-secondary/10 flex items-center justify-center shrink-0 overflow-hidden">
                            ${n.actor_avatar ? `<img src="${n.actor_avatar}" class="w-full h-full object-cover">` : `<span class="material-symbols-outlined text-secondary text-[16px]">forum</span>`}
                        </div>
                        <div>
                            <p class="text-label-md text-on-surface mb-1">${n.message}</p>
                            <p class="text-label-sm text-on-surface-variant">${new Date(n.created_at).toLocaleDateString()}</p>
                        </div>
                    </div>
                `).join('');
            }
        }
    }
}

async function readNotification(id) {
    const res = await apiRequest(`/notifications/${id}/read`, { method: 'PUT' });
    if (res.status === 200) {
        loadNotifications();
    }
}

// Bind dropdown toggle
document.addEventListener('DOMContentLoaded', () => {
    const notifBtn = document.getElementById('notificationBtn');
    if (notifBtn) {
        notifBtn.addEventListener('click', () => {
            const dropdown = document.getElementById('notificationDropdown');
            if (dropdown) dropdown.classList.toggle('hidden');
        });
    }
});
"""
    content += notif_logic

    # Also make populateUserProfile call loadNotifications
    content = content.replace("document.querySelectorAll('img[alt=\"Profile\"]').forEach(img => {", "loadNotifications();\n        document.querySelectorAll('img[alt=\"Profile\"]').forEach(img => {")

    with open(api_js_path, 'w') as f:
        f.write(content)
    
print("Added notification logic to api.js")

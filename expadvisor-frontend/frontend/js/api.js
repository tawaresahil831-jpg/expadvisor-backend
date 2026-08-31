const API_BASE = "https://expadvisor.onrender.com/api";

function getToken() {
    return localStorage.getItem("expadvisor_token");
}

function setToken(token) {
    localStorage.setItem("expadvisor_token", token);
}

function removeToken() {
    localStorage.removeItem("expadvisor_token");
}

async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    
    // Setup headers
    const headers = { ...options.headers };
    
    // Only set Content-Type if there is a body and it's not FormData
    if (options.body && !(options.body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
    }

    // Attach Token
    const token = getToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers
    };

    if (config.body && typeof config.body === 'object' && !(config.body instanceof FormData)) {
        config.body = JSON.stringify(config.body);
    }

    try {
        const response = await fetch(url, config);
        
        // Handle 401 Unauthorized globally
        if (response.status === 401) {
            removeToken();
            if (!window.location.pathname.endsWith('login.html') && !window.location.pathname.endsWith('register.html')) {
                window.location.href = 'login.html';
            }
        }
        
        let data;
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            data = await response.json();
        } else {
            const text = await response.text();
            data = { success: response.ok, message: text || `HTTP ${response.status} Error` };
        }
        return { status: response.status, data };
    } catch (error) {
        console.error("API Error:", error);
        return { status: 500, data: { success: false, message: error.message || "Network error" } };
    }
}

// Check if user is logged in
function requireAuth() {
    if (!getToken()) {
        window.location.href = 'login.html';
    }
}

// Fetch user profile and update DOM
async function populateUserProfile() {
    const response = await apiRequest('/auth/me', { method: 'GET' });
    if (response.status === 200 && response.data.success) {
        const user = response.data.data;
        
        // Update elements if they exist on the page
        const nameEls = document.querySelectorAll('.user-name-display');
        const roleEls = document.querySelectorAll('.user-role-display');
        
        nameEls.forEach(el => el.textContent = user.name || 'User');
        
        const formattedRole = user.role ? user.role.charAt(0).toUpperCase() + user.role.slice(1) : 'Student';
        roleEls.forEach(el => el.textContent = formattedRole);
        
        if (user.avatar_url) {
            const avatarEls = document.querySelectorAll('img[alt="Profile"]');
            avatarEls.forEach(el => el.src = user.avatar_url);
        } else {
            const avatarEls = document.querySelectorAll('img[alt="Profile"]');
            avatarEls.forEach(el => {
                const initial = (user.name || 'U').charAt(0).toUpperCase();
                const div = document.createElement('div');
                div.className = 'w-9 h-9 rounded-full bg-secondary/20 flex items-center justify-center text-secondary font-bold ring-2 ring-surface-variant';
                div.textContent = initial;
                el.parentNode.replaceChild(div, el);
            });
        }
        
        updateNotificationBadge();
        return user;
    }
    return null;
}

async function updateNotificationBadge() {
    if (!getToken()) return;
    try {
        const res = await apiRequest('/notifications/unread-count');
        if (res.status === 200 && res.data.success) {
            const count = res.data.data.unread_count || 0;
            const badgeEls = document.querySelectorAll('#notificationBadge, .notification-badge, [data-notification-badge]');
            badgeEls.forEach(el => {
                if (count > 0) {
                    el.textContent = count > 99 ? '99+' : count;
                    el.classList.remove('hidden');
                } else {
                    el.classList.add('hidden');
                }
            });
        }
    } catch (e) {
        console.error('Error updating notification badge:', e);
    }
}

async function toggleBookmark(experienceId) {
    return await apiRequest(`/experiences/${experienceId}/bookmark`, { method: 'POST' });
}

async function fetchBookmarks() {
    return await apiRequest('/bookmarks', { method: 'GET' });
}

function logout() {
    let modal = document.getElementById('logoutConfirmModal');
    if (!modal) {
        modal = document.createElement('dialog');
        modal.id = 'logoutConfirmModal';
        modal.className = 'rounded-3xl shadow-2xl p-0 w-full max-w-sm bg-white border border-slate-200 overflow-hidden text-slate-800 backdrop:bg-slate-900/50 backdrop:backdrop-blur-sm';
        modal.innerHTML = `
            <div class="p-6 text-center space-y-4">
                <div class="w-14 h-14 rounded-2xl bg-rose-50 text-rose-600 mx-auto flex items-center justify-center border border-rose-100 shadow-xs">
                    <span class="material-symbols-outlined text-[28px]">logout</span>
                </div>
                <div class="space-y-1.5">
                    <h3 class="text-base font-bold text-slate-900">Do you really want to log out?</h3>
                    <p class="text-xs text-slate-500 leading-relaxed px-2">
                        You will be logged out of your EXPadviser account on this device and will need to sign in again.
                    </p>
                </div>
                <div class="flex gap-2.5 pt-2">
                    <button type="button" onclick="document.getElementById('logoutConfirmModal').close()" class="flex-1 px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 transition-colors">
                        Cancel
                    </button>
                    <button type="button" onclick="confirmLogoutAction()" class="flex-1 px-4 py-2.5 rounded-xl text-xs font-semibold text-white bg-rose-600 hover:bg-rose-700 shadow-sm transition-colors flex items-center justify-center gap-1.5">
                        <span class="material-symbols-outlined text-[15px]">logout</span>
                        <span>Yes, Log Out</span>
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }
    modal.showModal();
}

function confirmLogoutAction() {
    removeToken();
    try {
        localStorage.removeItem('expadvisor_user');
    } catch(e) {}
    window.location.href = 'login.html';
}

// Global UI Bindings
document.addEventListener('DOMContentLoaded', () => {
    // Notification Dropdown Logic
    const notifBtn = document.getElementById('notificationBtn');
    const notifDropdown = document.getElementById('notificationDropdown');
    if (notifBtn && notifDropdown) {
        if (!notifBtn.dataset.bound) {
            notifBtn.dataset.bound = 'true';
            notifBtn.addEventListener('click', (e) => {
                notifDropdown.classList.toggle('hidden');
                if (!notifDropdown.classList.contains('hidden')) {
                    loadNotifications();
                }
                e.stopPropagation();
            });
            document.addEventListener('click', (e) => {
                if (!notifDropdown.contains(e.target) && e.target !== notifBtn) {
                    notifDropdown.classList.add('hidden');
                }
            });
        }
    }

    // Automatically load notifications on page load if user is logged in
    if (getToken()) {
        loadNotifications();
    }
});

// ====== NOTIFICATION LOGIC ======
async function loadNotifications() {
    if (!getToken()) return;

    try {
        const res = await apiRequest('/notifications');
        if (res.status === 200 && res.data && res.data.success) {
            const notifications = res.data.data || [];
            renderNotifications(notifications);
        }
    } catch (e) {
        console.warn('Could not load notifications:', e);
    }
}

function renderNotifications(notifications) {
    const dropdownContainer = document.getElementById('notifList') || 
                              document.querySelector('#notificationDropdown .overflow-y-auto') || 
                              document.querySelector('#notificationDropdown .max-h-80') || 
                              document.querySelector('#notificationDropdown .max-h-64') ||
                              document.querySelector('#notificationDropdown > div:nth-child(2)');
    const badges = document.querySelectorAll('#notifDot, #notificationBtn .bg-rose-500, #notificationBtn span.absolute');
    const unreadCountBadge = document.getElementById('notifUnreadBadge');
    
    const unreadCount = notifications.filter(n => !n.is_read).length;
    
    // Update red dot on notification bell button
    badges.forEach(badge => {
        if (unreadCount > 0) {
            badge.classList.remove('hidden');
            badge.style.display = 'block';
        } else {
            badge.classList.add('hidden');
            badge.style.display = 'none';
        }
    });

    // Update unread count badge in header
    if (unreadCountBadge) {
        if (unreadCount > 0) {
            unreadCountBadge.textContent = `${unreadCount} new`;
            unreadCountBadge.classList.remove('hidden');
        } else {
            unreadCountBadge.classList.add('hidden');
        }
    }
    
    if (dropdownContainer) {
        if (!notifications || notifications.length === 0) {
            dropdownContainer.innerHTML = `
                <div class="p-6 text-center text-slate-400 dark:text-slate-500 text-xs flex flex-col items-center gap-2">
                    <span class="material-symbols-outlined text-[28px] text-slate-300 dark:text-slate-600">notifications_none</span>
                    <span>All caught up! No new notifications.</span>
                </div>
            `;
        } else {
            dropdownContainer.innerHTML = notifications.map(n => {
                const isUnread = !n.is_read;
                const timeStr = n.created_at ? formatNotifTime(n.created_at) : 'Recently';
                
                return `
                    <div onclick="readNotification(${n.id}, ${n.experience_id || 'null'})" class="p-3.5 hover:bg-slate-50 dark:hover:bg-slate-800/60 transition-colors cursor-pointer flex gap-3 items-start ${isUnread ? 'bg-blue-50/50 dark:bg-blue-950/20' : 'opacity-75'}">
                        <div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300 flex items-center justify-center shrink-0 overflow-hidden font-bold text-xs">
                            ${n.actor_avatar 
                                ? `<img src="${n.actor_avatar}" class="w-full h-full object-cover">` 
                                : (n.actor_name ? n.actor_name.charAt(0).toUpperCase() : '<span class="material-symbols-outlined text-[16px]">notifications</span>')
                            }
                        </div>
                        <div class="flex-1 min-w-0">
                            <p class="text-xs ${isUnread ? 'font-semibold text-slate-900 dark:text-slate-100' : 'text-slate-700 dark:text-slate-300'} leading-snug">
                                ${escapeNotifHtml(n.message)}
                            </p>
                            <div class="flex items-center gap-2 mt-1">
                                <span class="text-[10px] text-slate-400 font-medium">${timeStr}</span>
                                ${n.experience_id ? '<span class="text-[10px] text-blue-600 dark:text-blue-400 font-semibold hover:underline">View query →</span>' : ''}
                            </div>
                        </div>
                        ${isUnread ? '<span class="w-2 h-2 rounded-full bg-blue-600 shrink-0 mt-1"></span>' : ''}
                    </div>
                `;
            }).join('');
        }
    }
}

function formatNotifTime(dateString) {
    try {
        if (dateString && !dateString.endsWith('Z') && !dateString.match(/[+-]\d{2}:\d{2}$/)) {
            dateString += 'Z';
        }
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / (1000 * 60));
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays}d ago`;
        return date.toLocaleDateString();
    } catch(e) {
        return 'Recently';
    }
}

function escapeNotifHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

async function readNotification(id, experienceId) {
    try {
        await apiRequest(`/notifications/${id}/read`, { method: 'PUT' });
        loadNotifications();
    } catch(e) {}

    if (experienceId) {
        if (window.location.pathname.includes('dashboard.html')) {
            const card = document.getElementById(`exp-${experienceId}`);
            if (card) {
                card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                card.classList.add('ring-2', 'ring-blue-500');
                setTimeout(() => card.classList.remove('ring-2', 'ring-blue-500'), 3000);
            }
        } else {
            window.location.href = `dashboard.html#exp-${experienceId}`;
        }
    }
}

async function markAllNotificationsRead() {
    const markBtn = document.getElementById('markAllReadBtn');
    if (markBtn) {
        markBtn.disabled = true;
        markBtn.innerHTML = '<span class="material-symbols-outlined text-[13px] animate-spin">sync</span> Marking...';
    }

    try {
        const res = await apiRequest('/notifications/read-all', { method: 'PUT' });
        if (res.status === 200 || (res.data && res.data.success)) {
            showToast('All notifications marked as read');
        }
    } catch(e) {
        console.error('Failed to mark all notifications read:', e);
    }

    await loadNotifications();

    if (markBtn) {
        markBtn.disabled = false;
        markBtn.innerHTML = '<span class="material-symbols-outlined text-[13px]">done_all</span><span>Mark all read</span>';
    }
}

// ====== GLOBAL DARK THEME MANAGEMENT ======
function initGlobalTheme() {
    const savedTheme = localStorage.getItem('exp_theme') || 'light';
    applyGlobalTheme(savedTheme);

    const headerToggle = document.getElementById('headerThemeToggle');
    const profileToggle = document.getElementById('themeToggleBtn');

    const toggleHandler = (e) => {
        if (e) e.preventDefault();
        const isDark = document.documentElement.classList.contains('dark');
        applyGlobalTheme(isDark ? 'light' : 'dark');
    };

    if (headerToggle) headerToggle.onclick = toggleHandler;
    if (profileToggle) profileToggle.onclick = toggleHandler;
}

function applyGlobalTheme(theme) {
    const isDark = theme === 'dark';
    if (isDark) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('exp_theme', 'dark');
    } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('exp_theme', 'light');
    }

    // Update icons on whatever page is active
    const headerIcon = document.getElementById('headerThemeIcon');
    if (headerIcon) headerIcon.textContent = isDark ? 'light_mode' : 'dark_mode';

    const toggleIcon = document.getElementById('themeToggleIcon');
    if (toggleIcon) toggleIcon.textContent = isDark ? 'light_mode' : 'dark_mode';

    const toggleText = document.getElementById('themeToggleText');
    if (toggleText) toggleText.textContent = isDark ? 'Light Mode' : 'Dark Mode';
}

// Immediately apply saved theme on parse & after DOMContentLoaded
(function() {
    try {
        const saved = localStorage.getItem('exp_theme') || 'light';
        if (saved === 'dark') document.documentElement.classList.add('dark');
    } catch(e) {}
})();

if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initGlobalTheme);
    } else {
        initGlobalTheme();
    }
}

// ====== SAVED / BOOKMARKED QUERIES SYSTEM ======
function getSavedQueriesKey() {
    try {
        const user = JSON.parse(localStorage.getItem('expadvisor_user') || '{}');
        const userId = user.user_id || user.id || 'default';
        return `expadvisor_saved_queries_${userId}`;
    } catch(e) {
        return 'expadvisor_saved_queries_default';
    }
}

function getSavedQueries() {
    try {
        const key = getSavedQueriesKey();
        return JSON.parse(localStorage.getItem(key) || '[]');
    } catch(e) {
        return [];
    }
}

function isQuerySaved(experienceId) {
    if (!experienceId) return false;
    const saved = getSavedQueries();
    return saved.some(q => String(q.experience_id) === String(experienceId));
}

function toggleSaveQuery(experience) {
    if (!experience) return false;
    const expId = typeof experience === 'object' ? experience.experience_id : experience;
    let saved = getSavedQueries();
    const index = saved.findIndex(q => String(q.experience_id) === String(expId));
    let isNowSaved = false;

    if (index >= 0) {
        saved.splice(index, 1);
        isNowSaved = false;
        showToast('Query removed from Saved');
    } else {
        const itemToSave = typeof experience === 'object' ? {
            experience_id: experience.experience_id,
            title: experience.title || 'Untitled Query',
            content: experience.content || '',
            category: experience.category || 'General',
            company: experience.company || '',
            author_name: experience.author_name || 'Anonymous',
            created_at: experience.created_at || new Date().toISOString(),
            is_resolved: !!experience.is_resolved,
            likes_count: experience.likes_count || 0,
            comments_count: experience.comments_count || 0
        } : { experience_id: expId, title: `Query #${expId}` };

        saved.unshift(itemToSave);
        isNowSaved = true;
        showToast('Query saved to your Profile!');
    }

    const key = getSavedQueriesKey();
    localStorage.setItem(key, JSON.stringify(saved));

    // Dispatch global event for live sync across components & tabs
    window.dispatchEvent(new CustomEvent('savedQueriesUpdated', { 
        detail: { experienceId: expId, isSaved: isNowSaved, totalSaved: saved.length } 
    }));

    return isNowSaved;
}

// Lightweight Toast Notification
function showToast(message) {
    let toast = document.getElementById('expToastPill');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'expToastPill';
        toast.className = 'fixed bottom-6 right-6 z-50 bg-slate-900 text-white px-4 py-2.5 rounded-2xl shadow-2xl text-xs font-semibold flex items-center gap-2 border border-slate-700 transition-all duration-300 transform translate-y-12 opacity-0 pointer-events-none';
        document.body.appendChild(toast);
    }

    toast.innerHTML = `
        <span class="material-symbols-outlined text-[18px] text-blue-400">bookmark</span>
        <span>${message}</span>
    `;

    toast.classList.remove('translate-y-12', 'opacity-0', 'pointer-events-none');
    toast.classList.add('translate-y-0', 'opacity-100');

    clearTimeout(window.__toastTimeout);
    window.__toastTimeout = setTimeout(() => {
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('translate-y-12', 'opacity-0', 'pointer-events-none');
    }, 2800);
}


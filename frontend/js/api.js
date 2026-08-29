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
        
        return user;
    }
    return null;
}

function logout() {
    removeToken();
    window.location.href = 'login.html';
}

// Global UI Bindings
document.addEventListener('DOMContentLoaded', () => {
    // Notification Dropdown Logic
    const notifBtn = document.getElementById('notificationBtn');
    const notifDropdown = document.getElementById('notificationDropdown');
    if (notifBtn && notifDropdown) {
        // Prevent multiple bindings if already bound elsewhere
        if (!notifBtn.dataset.bound) {
            notifBtn.dataset.bound = 'true';
            notifBtn.addEventListener('click', (e) => {
                notifDropdown.classList.toggle('hidden');
                e.stopPropagation();
            });
            document.addEventListener('click', (e) => {
                if (!notifDropdown.contains(e.target) && e.target !== notifBtn) {
                    notifDropdown.classList.add('hidden');
                }
            });
        }
    }
});


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


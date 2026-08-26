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
    
    // Only set Content-Type if it's not FormData
    if (!(options.body instanceof FormData)) {
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
        
        const data = await response.json();
        return { status: response.status, data };
    } catch (error) {
        console.error("API Error:", error);
        return { status: 500, data: { success: false, message: "Network error" } };
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
        
        // Format role (e.g., 'student' -> 'Student', 'mentor' -> 'Mentor')
        const formattedRole = user.role ? user.role.charAt(0).toUpperCase() + user.role.slice(1) : 'Student';
        roleEls.forEach(el => el.textContent = formattedRole);
        
        return user;
    }
    return null;
}

function logout() {
    removeToken();
    window.location.href = 'login.html';
}

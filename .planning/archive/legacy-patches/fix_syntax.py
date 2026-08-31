import re

files = [
    '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/login.html',
    '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/register.html'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the orphaned code and remove it
    orphaned_code = """    if (response.status !== 200) {
        response = await apiRequest('/auth/register', { method: 'POST', body: { name: name.trim(), email: email.trim(), password: 'google_sso_' + email.trim() } });
    }
    if (response.status === 200 || response.status === 201) {
        setToken(response.data.data.token);
        window.location.href = 'dashboard.html';
    } else {
        errorMsg.textContent = 'Google Sign In failed.';
        errorMsg.classList.remove('hidden');
    }
  });"""
    content = content.replace(orphaned_code, "")
    
    # Also in login.html there might be slightly different orphaned code
    orphaned_code_2 = """    let response = await apiRequest('/auth/login', {
        method: 'POST',
        body: { email: email.trim(), password: 'google_sso_' + email.trim() }
    });
    
    if (response.status !== 200) {
        const name = prompt('First time? Enter your name:');
        if (!name || !name.trim()) return;
        
        response = await apiRequest('/auth/register', {
            method: 'POST',
            body: { name: name.trim(), email: email.trim(), password: 'google_sso_' + email.trim() }
        });
    }
    
    if (response.status === 200 || response.status === 201) {
        setToken(response.data.data.token);
        window.location.href = 'dashboard.html';
    } else {
        errorMsg.textContent = 'Google Sign In failed: ' + (response.data ? response.data.message : 'Unknown error');
        errorMsg.classList.remove('hidden');
    }
  });"""
    content = content.replace(orphaned_code_2, "")

    with open(filepath, 'w') as f:
        f.write(content)
print("Done fixing syntax")

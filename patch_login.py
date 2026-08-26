import re
filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/login.html'
with open(filepath, 'r') as f:
    content = f.read()

bad_script = """<script>
  if (getToken()) window.location.href = 'dashboard.html';

  
    
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

good_script = """<script>
  if (getToken()) window.location.href = 'dashboard.html';

  async function handleCredentialResponse(googleResponse) {
    const errorMsg = document.getElementById('errorMsg');
    
    const response = await apiRequest('/auth/google', {
      method: 'POST',
      body: { token: googleResponse.credential }
    });
    
    if (response.status === 200 || response.status === 201) {
      setToken(response.data.data.token);
      window.location.href = 'dashboard.html';
    } else {
      errorMsg.textContent = 'Google Sign In failed: ' + (response.data && response.data.message ? response.data.message : 'Unknown error');
      errorMsg.classList.remove('hidden');
    }
  }

  window.onload = function () {
    google.accounts.id.initialize({
      client_id: "264177546521-l4f6okrlas9sk890h9elaj17ce6ok5h7.apps.googleusercontent.com",
      callback: handleCredentialResponse
    });
    google.accounts.id.renderButton(
      document.getElementById("googleBtnContainer"),
      { theme: "outline", size: "large", width: 280 }
    );
  };
"""

content = content.replace(bad_script, good_script)
with open(filepath, 'w') as f:
    f.write(content)

print("Done patching login.html")

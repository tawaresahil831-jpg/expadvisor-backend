import re

files = [
    '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/login.html',
    '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/register.html'
]

CLIENT_ID = "264177546521-l4f6okrlas9sk890h9elaj17ce6ok5h7.apps.googleusercontent.com"

# The div to insert
gsi_div = f"""
        <div id="googleBtnContainer" class="w-full flex justify-center mt-2"></div>
"""

# The script to insert
gsi_script = f"""
<script src="https://accounts.google.com/gsi/client" async defer></script>
<script>
  function handleGoogleLogin(response) {{
    const errorMsg = document.getElementById('errorMessage');
    if(errorMsg) errorMsg.classList.add('hidden');
    
    apiRequest('/auth/google', {{
        method: 'POST',
        body: {{ credential: response.credential }}
    }}).then(res => {{
        if (res.status === 200 || res.status === 201) {{
            setToken(res.data.data.token);
            window.location.href = 'dashboard.html';
        }} else {{
            if(errorMsg) {{
                errorMsg.textContent = 'Google Sign In failed: ' + (res.data ? res.data.message : 'Unknown error');
                errorMsg.classList.remove('hidden');
            }} else {{
                alert('Google Sign In failed');
            }}
        }}
    }}).catch(err => {{
        console.error(err);
        if(errorMsg) {{
            errorMsg.textContent = 'Network error during Google Sign In';
            errorMsg.classList.remove('hidden');
        }}
    }});
  }}

  window.addEventListener('load', function () {{
    google.accounts.id.initialize({{
      client_id: "{CLIENT_ID}",
      callback: handleGoogleLogin
    }});
    
    const btnContainer = document.getElementById("googleBtnContainer");
    if(btnContainer) {{
        google.accounts.id.renderButton(
          btnContainer,
          {{ theme: "outline", size: "large", width: 400 }}  
        );
    }}
  }});
</script>
"""

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove the old dummy googleBtn block
    if '<button id="googleBtn"' in content:
        # Regex to remove the entire <button id="googleBtn" ... </button> block
        content = re.sub(r'<button id="googleBtn".*?</button>', gsi_div, content, flags=re.DOTALL)
    
    # Remove the old googleBtn event listener
    if "document.getElementById('googleBtn').addEventListener('click'" in content:
        content = re.sub(r"document\.getElementById\('googleBtn'\)\.addEventListener\('click', async \(\) => \{.*?\}\);", "", content, flags=re.DOTALL)
        
    # Insert the GSI script right before </body>
    if '<script src="https://accounts.google.com/gsi/client"' not in content:
        content = content.replace('</body>', gsi_script + '\n</body>')
        
    with open(filepath, 'w') as f:
        f.write(content)
        
    print(f"Patched {filepath}")


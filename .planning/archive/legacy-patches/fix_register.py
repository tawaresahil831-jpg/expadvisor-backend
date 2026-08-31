import re

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/register.html'
with open(filepath, 'r') as f:
    content = f.read()

# Remove hardcoded values
content = content.replace(' value="XYZ"', '')
content = content.replace(' value="pass123"', '')

# Add IDs to the password toggle buttons so we can easily target them
# First toggle button (Set Password)
content = re.sub(
    r'<button class="absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant hover:text-primary transition-colors" type="button" style="color:#45474c;">\s*<span class="material-symbols-outlined text-\[20px\]">visibility</span>\s*</button>',
    '<button id="togglePassword" class="absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant hover:text-primary transition-colors" type="button" style="color:#45474c;"><span class="material-symbols-outlined text-[20px]" id="togglePasswordIcon">visibility</span></button>',
    content
)

# Second toggle button (Confirm Password)
content = re.sub(
    r'<button class="absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant hover:text-primary transition-colors" type="button" style="color:#45474c;">\s*<span class="material-symbols-outlined text-\[20px\]">visibility_off</span>\s*</button>',
    '<button id="toggleConfirmPassword" class="absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant hover:text-primary transition-colors" type="button" style="color:#45474c;"><span class="material-symbols-outlined text-[20px]" id="toggleConfirmPasswordIcon">visibility_off</span></button>',
    content
)

# Add the JavaScript for toggling passwords
toggle_script = """
<script>
  document.getElementById('togglePassword').addEventListener('click', function() {
    const pwdInput = document.getElementById('password');
    const pwdIcon = document.getElementById('togglePasswordIcon');
    if (pwdInput.type === 'password') {
      pwdInput.type = 'text';
      pwdIcon.textContent = 'visibility_off';
    } else {
      pwdInput.type = 'password';
      pwdIcon.textContent = 'visibility';
    }
  });

  document.getElementById('toggleConfirmPassword').addEventListener('click', function() {
    const pwdInput = document.getElementById('confirmPassword');
    const pwdIcon = document.getElementById('toggleConfirmPasswordIcon');
    if (pwdInput.type === 'password') {
      pwdInput.type = 'text';
      pwdIcon.textContent = 'visibility';
    } else {
      pwdInput.type = 'password';
      pwdIcon.textContent = 'visibility_off';
    }
  });
</script>
</body>
"""

if "document.getElementById('togglePassword')" not in content:
    content = content.replace('</body>', toggle_script)

with open(filepath, 'w') as f:
    f.write(content)
print("Done")

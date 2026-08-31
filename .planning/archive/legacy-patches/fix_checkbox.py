filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/register.html'
with open(filepath, 'r') as f:
    content = f.read()

# Add ID to checkbox
content = content.replace('<input class="peer sr-only" type="checkbox">', '<input id="termsCheckbox" class="peer sr-only" type="checkbox">')

# Add validation logic to the submit handler
validation_logic = """    if (password !== confirmPassword) {
        errorMsg.textContent = 'Passwords do not match.';
        errorMsg.classList.remove('hidden');
        return;
    }
    
    const termsChecked = document.getElementById('termsCheckbox').checked;
    if (!termsChecked) {
        errorMsg.textContent = 'You must agree to the Terms & Conditions and Privacy Policy.';
        errorMsg.classList.remove('hidden');
        return;
    }"""

content = content.replace("""    if (password !== confirmPassword) {
        errorMsg.textContent = 'Passwords do not match.';
        errorMsg.classList.remove('hidden');
        return;
    }""", validation_logic)

with open(filepath, 'w') as f:
    f.write(content)

print("Done fixing checkbox")

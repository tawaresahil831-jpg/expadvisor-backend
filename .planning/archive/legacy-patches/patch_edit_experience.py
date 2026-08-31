import re
import os

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/dashboard.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add Edit button next to Delete button
edit_btn = """<button onclick="editExperience(${exp.experience_id})" class="p-1 text-on-surface-variant hover:text-secondary hover:bg-secondary/10 rounded-full transition-colors" title="Edit"><span class="material-symbols-outlined text-[18px]">edit</span></button>
                                <button onclick="deleteExperience(${exp.experience_id})\""""
content = content.replace('<button onclick="deleteExperience(${exp.experience_id})"', edit_btn)


# 2. Update form submit logic
# We'll inject a global variable for editing, and an editExperience function.
edit_logic = """
    let currentEditExpId = null;

    async function editExperience(id) {
        // Fetch details
        const res = await apiRequest(`/experiences/${id}`);
        if (res.status === 200 && res.data.success) {
            const exp = res.data.data;
            document.getElementById('expTitle').value = exp.title;
            document.getElementById('expCompany').value = exp.company || '';
            document.getElementById('expCategory').value = exp.category || 'General';
            document.getElementById('expDifficulty').value = exp.semester || 'All';
            document.getElementById('expDetails').value = exp.content || '';
            
            currentEditExpId = id;
            document.querySelector('#createModal h3').textContent = 'Edit Experience';
            const modal = document.getElementById('createModal');
            if (modal) modal.showModal();
        } else {
            alert('Failed to load experience details.');
        }
    }

    // Reset currentEditExpId when modal closes (e.g. Cancel button)
    document.querySelector('#createModal button[onclick="document.getElementById(\\'createModal\\').close()"]').addEventListener('click', () => {
        currentEditExpId = null;
        document.querySelector('#createModal h3').textContent = 'Ask a Query';
        document.getElementById('createExpForm').reset();
    });
"""

# Find where to insert edit_logic (before createExpForm submit listener)
insert_idx = content.find("document.getElementById('createExpForm').addEventListener('submit'")
content = content[:insert_idx] + edit_logic + "\n    " + content[insert_idx:]

# 3. Update the submit listener to handle PUT
submit_logic_old = """const response = await apiRequest('/experiences', {
            method: 'POST',
            body: requestBody
        });"""
        
submit_logic_new = """
        let endpoint = '/experiences';
        let reqMethod = 'POST';
        if (currentEditExpId) {
            endpoint = `/experiences/${currentEditExpId}`;
            reqMethod = 'PUT';
        }

        const response = await apiRequest(endpoint, {
            method: reqMethod,
            body: requestBody
        });"""

content = content.replace(submit_logic_old, submit_logic_new)

# 4. Handle success response appropriately
success_logic_old = """if (response.status === 201 && response.data.success) {"""
success_logic_new = """if ((response.status === 201 || response.status === 200) && response.data.success) {"""
content = content.replace(success_logic_old, success_logic_new)

# 5. Clean up after submit
reset_logic_old = """document.getElementById('createModal').close();
            e.target.reset();"""
reset_logic_new = """document.getElementById('createModal').close();
            e.target.reset();
            currentEditExpId = null;
            document.querySelector('#createModal h3').textContent = 'Ask a Query';"""
content = content.replace(reset_logic_old, reset_logic_new)

with open(filepath, 'w') as f:
    f.write(content)

print("Added edit experience functionality to dashboard.html")

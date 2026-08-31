import re

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/dashboard.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add id and onclick to the Load More button
load_more_old = '<button class="w-full py-4 text-center text-on-surface-variant font-label-md text-label-md hover:bg-surface-container-low rounded-xl transition-colors border border-dashed border-outline-variant/50">\n                            Load More Problems\n                        </button>'
load_more_new = '<button id="loadMoreBtn" onclick="loadMoreExperiences()" class="hidden w-full py-4 text-center text-on-surface-variant font-label-md text-label-md hover:bg-surface-container-low rounded-xl transition-colors border border-dashed border-outline-variant/50">\n                            Load More Problems\n                        </button>'
content = content.replace(load_more_old, load_more_new)

# 2. Add currentPage state
state_old = "let currentStatus = 'Open';"
state_new = "let currentStatus = 'Open';\n    let currentPage = 1;"
content = content.replace(state_old, state_new)

# 3. Update loadExperiences to accept append argument and handle pagination
load_exp_old = """    async function loadExperiences() {
        const container = document.getElementById('feedContainer');
        container.innerHTML = '<p class="text-center py-4">Loading...</p>';
        
        let endpoint = '/experiences';
        const params = [];
        if (currentSearch) params.push(`search=${encodeURIComponent(currentSearch)}`);
        if (currentCategory) params.push(`category=${encodeURIComponent(currentCategory)}`);
        if (params.length) endpoint += '?' + params.join('&');

        const response = await apiRequest(endpoint);
        
        if (response.status === 200 && response.data.success) {"""

load_exp_new = """    async function loadExperiences(append = false) {
        const container = document.getElementById('feedContainer');
        if (!append) {
            container.innerHTML = '<p class="text-center py-4">Loading...</p>';
        }
        
        let endpoint = '/experiences';
        const params = [];
        params.push(`page=${currentPage}`);
        if (currentSearch) params.push(`search=${encodeURIComponent(currentSearch)}`);
        if (currentCategory) params.push(`category=${encodeURIComponent(currentCategory)}`);
        if (params.length) endpoint += '?' + params.join('&');

        const response = await apiRequest(endpoint);
        
        if (response.status === 200 && response.data.success) {"""

content = content.replace(load_exp_old, load_exp_new)

# 4. Handle rendering with append and button visibility
render_old = """            if (expList.length === 0) {
                container.innerHTML = '<p class="text-center py-4">No experiences found.</p>';
                return;
            }
            
            container.innerHTML = expList.map(exp => `"""

render_new = """            if (expList.length === 0 && !append) {
                container.innerHTML = '<p class="text-center py-4">No experiences found.</p>';
                document.getElementById('loadMoreBtn').classList.add('hidden');
                return;
            }

            const html = expList.map(exp => `"""

content = content.replace(render_old, render_new)

# 5. Handle innerHTML insertion and Load More visibility
insertion_old = """                                    <span class="text-label-md text-secondary font-bold">${exp.comments_count}</span>
                                </button>
                                <button class="text-on-surface-variant hover:text-secondary transition-colors">
                                    <span class="material-symbols-outlined text-[20px]">bookmark</span>
                                </button>
                            </div>
                            <div class="flex gap-3">
                                <button onclick="openExperienceDetail(${exp.experience_id})" class="text-secondary font-label-md hover:underline ${exp.is_resolved ? 'font-bold' : ''}">View Query</button>
                                ${!exp.is_resolved ? `<button onclick="openExperienceDetail(${exp.experience_id})" class="bg-secondary/10 text-secondary px-4 py-1.5 rounded-lg font-label-md hover:bg-secondary/20 transition-colors">Answer</button>` : ''}
                            </div>
                        </div>
                    </article>
                `).join('');
        } else {
            container.innerHTML = '<p class="text-center py-4 text-error">Failed to load experiences.</p>';
        }
    }"""

insertion_new = """                                    <span class="text-label-md text-secondary font-bold">${exp.comments_count}</span>
                                </button>
                                <button class="text-on-surface-variant hover:text-secondary transition-colors">
                                    <span class="material-symbols-outlined text-[20px]">bookmark</span>
                                </button>
                            </div>
                            <div class="flex gap-3">
                                <button onclick="openExperienceDetail(${exp.experience_id})" class="text-secondary font-label-md hover:underline ${exp.is_resolved ? 'font-bold' : ''}">View Query</button>
                                ${!exp.is_resolved ? `<button onclick="openExperienceDetail(${exp.experience_id})" class="bg-secondary/10 text-secondary px-4 py-1.5 rounded-lg font-label-md hover:bg-secondary/20 transition-colors">Answer</button>` : ''}
                            </div>
                        </div>
                    </article>
                `).join('');
                
            if (append) {
                container.insertAdjacentHTML('beforeend', html);
            } else {
                container.innerHTML = html;
            }

            // Handle Load More button visibility
            const loadMoreBtn = document.getElementById('loadMoreBtn');
            if (currentPage < response.data.total_pages) {
                loadMoreBtn.classList.remove('hidden');
            } else {
                loadMoreBtn.classList.add('hidden');
            }
        } else {
            if (!append) container.innerHTML = '<p class="text-center py-4 text-error">Failed to load experiences.</p>';
        }
    }

    function loadMoreExperiences() {
        currentPage++;
        loadExperiences(true);
    }"""

content = content.replace(insertion_old, insertion_new)

# 6. Reset currentPage when filtering
filters = ["currentCategory = category;", "currentSearch = e.target.value;", "currentStatus = status;"]
for f in filters:
    content = content.replace(f, f + "\n        currentPage = 1;")

with open(filepath, 'w') as f:
    f.write(content)

print("Frontend pagination patched.")

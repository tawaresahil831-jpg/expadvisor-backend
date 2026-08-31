
    requireAuth();
    
    const notifBtn = document.getElementById('notificationBtn');
    const notifDropdown = document.getElementById('notificationDropdown');
    if (notifBtn && notifDropdown) {
        notifBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            notifDropdown.classList.toggle('hidden');
        });
        document.addEventListener('click', (e) => {
            if (!notifBtn.contains(e.target) && !notifDropdown.contains(e.target)) {
                notifDropdown.classList.add('hidden');
            }
        });
    }

    let currentUserId = null;
    populateUserProfile().then(u => {
        if (u) currentUserId = u.id || u.user_id;
    });

    document.addEventListener('DOMContentLoaded', () => {
        if (window.location.hash === '#ask') {
            const modal = document.getElementById('createModal');
            if (modal) modal.showModal();
            history.replaceState(null, null, ' '); // remove hash
        }
    });


    // Add category filter logic
    document.addEventListener('DOMContentLoaded', () => {
        const catBtns = document.querySelectorAll('.filter-cat-btn');
        catBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                // Remove active styling from all
                catBtns.forEach(b => {
                    b.classList.remove('bg-secondary', 'text-on-secondary', 'shadow-sm');
                    b.classList.add('bg-surface', 'text-on-surface-variant', 'border', 'border-outline-variant/30');
                });
                // Add active styling to clicked
                const target = e.currentTarget;
                target.classList.remove('bg-surface', 'text-on-surface-variant', 'border', 'border-outline-variant/30');
                target.classList.add('bg-secondary', 'text-on-secondary', 'shadow-sm');
                
                // Set currentCategory and reload
                currentCategory = target.textContent.trim() === 'All' ? '' : target.textContent.trim();
                loadExperiences();
            });
        });
        
        const statusBtns = document.querySelectorAll('.filter-status-btn');
        statusBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                // Toggle active state
                const target = e.currentTarget;
                if (target.classList.contains('bg-secondary')) {
                    // Deselect
                    target.classList.remove('bg-secondary', 'text-on-secondary', 'shadow-sm');
                    target.classList.add('bg-surface', 'text-on-surface-variant', 'border', 'border-outline-variant/30');
                    currentStatus = '';
                } else {
                    // Deselect all others
                    statusBtns.forEach(b => {
                        b.classList.remove('bg-secondary', 'text-on-secondary', 'shadow-sm');
                        b.classList.add('bg-surface', 'text-on-surface-variant', 'border', 'border-outline-variant/30');
                    });
                    // Select this one
                    target.classList.remove('bg-surface', 'text-on-surface-variant', 'border', 'border-outline-variant/30');
                    target.classList.add('bg-secondary', 'text-on-secondary', 'shadow-sm');
                    currentStatus = target.textContent.trim();
                }
                loadExperiences();
            });
        });

        // Trending topics click to search
        const hashtagBtns = document.querySelectorAll('.hashtag-btn');
        hashtagBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tag = e.currentTarget.textContent.trim().replace('#', '');
                currentSearch = tag;
                const searchInput = document.getElementById('searchInput');
                if (searchInput) searchInput.value = currentSearch;
                loadExperiences();
            });
        });
    });


    let currentSearch = '';
    let currentCategory = '';
    let currentStatus = '';


    
    function formatHashtags(text) {
        if (!text) return '';
        // Escape HTML to prevent XSS before parsing hashtags
        const escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
        return escaped.replace(/#(\w+)/g, '<span class="text-secondary font-semibold hover:underline cursor-pointer" onclick="event.stopPropagation(); setHashtagSearch(\'$1\')">#$1</span>');
    }

    function setHashtagSearch(tag) {
        currentSearch = tag;
        const searchInput = document.getElementById('searchInput');
        if (searchInput) searchInput.value = currentSearch;
        
        // Also try to match a category button if it's an exact match
        const catBtns = document.querySelectorAll('.filter-cat-btn');
        let matched = false;
        catBtns.forEach(b => {
            if (b.textContent.trim().toLowerCase() === tag.toLowerCase()) {
                b.click(); // This will trigger the category filter
                matched = true;
            }
        });
        
        // If it's not a category, just use the search filter
        if (!matched) {
            // Deselect all categories
            catBtns.forEach(b => {
                b.classList.remove('bg-secondary', 'text-on-secondary', 'shadow-sm');
                b.classList.add('bg-surface', 'text-on-surface-variant', 'border', 'border-outline-variant/30');
            });
            currentCategory = '';
            loadExperiences();
        }
    }

    async function loadExperiences() {
        const container = document.getElementById('feedContainer');
        container.innerHTML = '<p class="text-center py-4">Loading...</p>';
        
        let endpoint = '/experiences';
        const params = [];
        if (currentSearch) params.push(`search=${encodeURIComponent(currentSearch)}`);
        if (currentCategory) params.push(`category=${encodeURIComponent(currentCategory)}`);
        if (params.length) endpoint += '?' + params.join('&');

        const response = await apiRequest(endpoint);
        
        if (response.status === 200 && response.data.success) {
            let expList = response.data.data;
            
            // Update stats
            const total = expList.length;
            const answered = expList.filter(e => e.comments_count > 0).length;
            const uniqueUsers = new Set(expList.map(e => e.author_id));
            const contributors = uniqueUsers.size;
            
            if(document.getElementById('stat-total-queries')) document.getElementById('stat-total-queries').textContent = total;
            if(document.getElementById('stat-answered')) document.getElementById('stat-answered').textContent = answered;
            if(document.getElementById('stat-contributors')) document.getElementById('stat-contributors').textContent = contributors;
            if(document.getElementById('stat-members')) document.getElementById('stat-members').textContent = contributors + 12; // Mock total members

            if (currentStatus === 'Open') {
                expList = expList.filter(e => e.comments_count === 0);
            } else if (currentStatus === 'Answered') {
                expList = expList.filter(e => e.comments_count > 0);
            }

            if (expList.length === 0) {
                container.innerHTML = '<p class="text-center py-4">No experiences found.</p>';
                return;
            }
            
            container.innerHTML = expList.map(exp => `
                <article class="bg-surface rounded-2xl p-6 shadow-sm border border-outline-variant/10 hover:shadow-md transition-all flex flex-col gap-4">
                    <div class="flex justify-between items-start">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-full bg-secondary/20 flex items-center justify-center text-secondary font-bold">
                                ${(exp.author_name || 'U')[0].toUpperCase()}
                            </div>
                            <div class="flex flex-col">
                                <div class="flex items-center gap-2">
                                    <span class="font-label-md text-on-surface">${exp.author_name || 'Unknown'}</span>
                                    <span class="px-2 py-0.5 rounded bg-secondary/10 text-secondary text-[10px] font-bold uppercase">${exp.semester || 'All'}</span>
                                </div>
                            </div>
                        </div>
                        <div class="flex items-center gap-2">
                            ${exp.author_id === currentUserId ? `
                                <button onclick="editExperience(${exp.experience_id})" class="p-1 text-on-surface-variant hover:text-secondary hover:bg-secondary/10 rounded-full transition-colors" title="Edit"><span class="material-symbols-outlined text-[18px]">edit</span></button>
                                <button onclick="deleteExperience(${exp.experience_id})" class="p-1 text-on-surface-variant hover:text-error hover:bg-error/10 rounded-full transition-colors" title="Delete"><span class="material-symbols-outlined text-[18px]">delete</span></button>
                            ` : ''}
                        </div>
                    </div>
                    <div>
                        <h3 onclick="openExperienceDetail(${exp.experience_id})" class="font-headline-md text-headline-md text-on-surface mb-2 hover:text-secondary cursor-pointer transition-colors">${formatHashtags(exp.title)}</h3>
                        <p onclick="openExperienceDetail(${exp.experience_id})" class="font-body-md text-on-surface-variant line-clamp-2 cursor-pointer">${formatHashtags(exp.content)}</p>
                    </div>
                    <div class="flex flex-wrap gap-2">
                        <span class="px-2.5 py-1 rounded-md bg-surface-container-high text-on-surface-variant font-label-sm">${exp.category || 'General'}</span>
                        <span class="px-2.5 py-1 rounded-md border border-outline-variant/30 text-on-surface-variant font-label-sm">${exp.company || 'Company'}</span>
                    </div>
                    <div class="flex items-center justify-between pt-4 border-t border-outline-variant/10">
                        <div class="flex items-center gap-6">
                            <button onclick="likeExperience(${exp.experience_id}, this)" class="flex items-center gap-1.5 text-on-surface-variant hover:text-secondary transition-colors">
                                <span class="material-symbols-outlined text-[20px]">thumb_up</span>
                                <span class="text-label-md" id="like-count-${exp.experience_id}">${exp.likes_count || 0}</span>
                            </button>
                            <button onclick="openExperienceDetail(${exp.experience_id})" class="flex items-center gap-1.5 text-on-surface-variant hover:text-secondary transition-colors">
                                <span class="material-symbols-outlined text-[20px]">chat_bubble</span>
                                <span class="text-label-md">${exp.comments_count || 0}</span>
                            </button>
                            <div class="flex items-center gap-1.5 text-on-surface-variant" title="Views">
                                <span class="material-symbols-outlined text-[20px]">visibility</span>
                                <span class="text-label-md">${exp.views || 0}</span>
                            </div>
                            ${exp.file_url ? `
                            <a href="${exp.file_url}" target="_blank" class="flex items-center gap-1.5 text-on-surface-variant hover:text-secondary transition-colors" title="Attachment">
                                <span class="material-symbols-outlined text-[20px]">attachment</span>
                            </a>
                            ` : ''}
                        </div>
                        <div class="flex items-center gap-3">
                            <button onclick="openExperienceDetail(${exp.experience_id})" class="text-secondary font-label-md hover:underline">View Query</button>
                            <button onclick="openExperienceDetail(${exp.experience_id})" class="bg-surface-container text-on-surface font-label-md py-1.5 px-4 rounded-lg hover:bg-surface-container-high transition-colors border border-outline-variant/20 shadow-sm">Answer</button>
                        </div>
                    </div>
                </article>
            `).join('');
        } else {
            container.innerHTML = '<p class="text-error text-center py-4">Failed to load experiences.</p>';
        }
    }

    async function likeExperience(id, btn) {
        const response = await apiRequest(`/experiences/${id}/like`, { method: 'POST' });
        if (response.status === 200 || response.status === 201) {
            const countEl = document.getElementById(`like-count-${id}`);
            if (countEl) countEl.textContent = response.data.data.like_count;
            if (btn) btn.classList.add('text-secondary');
        }
    }

    async function deleteExperience(id) {
        if (!confirm('Are you sure you want to delete this experience?')) return;
        const response = await apiRequest(`/experiences/${id}`, { method: 'DELETE' });
        if (response.status === 200 && response.data.success) {
            loadExperiences();
        } else {
            alert(response.data.message || 'Failed to delete experience');
        }
    }

    let currentDetailExpId = null;
    async function openExperienceDetail(id) {
        currentDetailExpId = id;
        const modal = document.getElementById('detailModal');
        
        document.getElementById('detailTitle').textContent = 'Loading...';
        document.getElementById('detailDescription').textContent = '...';
        document.getElementById('detailTags').innerHTML = '';
        document.getElementById('detailAttachmentContainer').classList.add('hidden');
        document.getElementById('detailComments').innerHTML = '<p class="text-center text-on-surface-variant text-sm py-4">Loading comments...</p>';
        document.getElementById('commentInput').value = '';
        
        modal.showModal();
        
        const response = await apiRequest(`/experiences/${id}`);
        if (response.status === 200 && response.data.success) {
            const exp = response.data.data;
            document.getElementById('detailTitle').innerHTML = formatHashtags(exp.title);
            document.getElementById('detailDescription').innerHTML = formatHashtags(exp.content);
            
            document.getElementById('detailTags').innerHTML = `
                <span class="px-2.5 py-1 rounded-md bg-surface-container-high text-on-surface-variant font-label-sm text-label-sm tracking-wider uppercase">${exp.category || 'General'}</span>
            `;
            
            if (exp.file_url) {
                document.getElementById('detailAttachmentContainer').classList.remove('hidden');
                document.getElementById('detailAttachmentLink').href = exp.file_url;
            }
            
                        // Fetch comments separately since they aren't included in the experience object
            const commentsRes = await apiRequest(`/experiences/${id}/comments`);
            let comments = [];
            if (commentsRes.status === 200 && commentsRes.data.success) {
                comments = commentsRes.data.data;
            }
            renderComments(comments);
        }
    }
    

    async function deleteComment(id) {
        if (confirm("Are you sure you want to delete this comment?")) {
            const res = await apiRequest(`/comments/${id}`, { method: 'DELETE' });
            if (res.status === 200) {
                openExperienceDetail(currentDetailExpId);
            } else {
                alert('Failed to delete comment: ' + (res.data?.message || ''));
            }
        }
    }

    async function editComment(id, currentText) {
        const newText = prompt("Edit your comment:", currentText);
        if (newText !== null && newText.trim() !== currentText && newText.trim() !== "") {
            const res = await apiRequest(`/comments/${id}`, {
                method: 'PUT',
                body: { comment: newText.trim() }
            });
            if (res.status === 200) {
                openExperienceDetail(currentDetailExpId);
            } else {
                alert('Failed to edit comment: ' + (res.data?.message || ''));
            }
        }
    }

    function renderComments(comments) {
        const container = document.getElementById('detailComments');
        if (comments.length === 0) {
            container.innerHTML = '<p class="text-center text-on-surface-variant text-sm py-4">No comments yet. Be the first to comment!</p>';
            return;
        }
        
        container.innerHTML = comments.map(c => `
            <div class="bg-surface-container-low p-4 rounded-xl border border-outline-variant/20">
                <div class="flex justify-between items-center mb-1">
                    <span class="font-label-md text-on-surface" style="font-weight:600;">${c.user_name || 'User'}</span>
                    <div class="flex items-center gap-2">
                        <span class="text-[11px] text-on-surface-variant">${new Date(c.created_at).toLocaleString([], {year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit'})}</span>
                        ${(currentUserId && c.user_id === currentUserId) ? `
                            <button onclick="editComment(${c.comment_id}, \`${c.comment.replace(/`/g, "'")}\`)" class="text-secondary hover:text-primary transition-colors text-[14px]">
                                <span class="material-symbols-outlined" style="font-size: 16px;">edit</span>
                            </button>
                            <button onclick="deleteComment(${c.comment_id})" class="text-error hover:text-error/80 transition-colors text-[14px]">
                                <span class="material-symbols-outlined" style="font-size: 16px;">delete</span>
                            </button>
                        ` : ''}
                    </div>
                </div>
                <p class="text-body-sm text-on-surface-variant">${c.comment}</p>
            </div>
        `).join('');
    }
    
    document.getElementById('commentForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!currentDetailExpId) return;
        
        const content = document.getElementById('commentInput').value.trim();
        if (!content) return;
        
        const btn = document.getElementById('submitCommentBtn');
        btn.disabled = true;
        btn.textContent = 'Posting...';
        
        const response = await apiRequest(`/experiences/${currentDetailExpId}/comments`, {
            method: 'POST',
            body: { comment: content }
        });
        
        if ((response.status === 201 || response.status === 200) && response.data.success) {
            document.getElementById('commentInput').value = '';
            openExperienceDetail(currentDetailExpId);
        } else {
            alert(response.data.message || 'Failed to post comment');
        }
        
        btn.disabled = false;
        btn.textContent = 'Post';
    });

    
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
    document.querySelector('#createModal button[onclick="document.getElementById(\'createModal\').close()"]').addEventListener('click', () => {
        currentEditExpId = null;
        document.querySelector('#createModal h3').textContent = 'Ask a Query';
        document.getElementById('createExpForm').reset();
    });

    document.getElementById('createExpForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = document.getElementById('submitExpBtn');
        btn.disabled = true;
        btn.textContent = 'Submitting...';

        const requestBody = {
            title: document.getElementById('expTitle').value,
            company: document.getElementById('expCompany').value,
            category: document.getElementById('expCategory').value,
            semester: document.getElementById('expDifficulty').value,
            content: document.getElementById('expDetails').value
        };

        
        let endpoint = '/experiences';
        let reqMethod = 'POST';
        if (currentEditExpId) {
            endpoint = `/experiences/${currentEditExpId}`;
            reqMethod = 'PUT';
        }

        const response = await apiRequest(endpoint, {
            method: reqMethod,
            body: requestBody
        });

        if ((response.status === 201 || response.status === 200) && response.data.success) {
            const expId = response.data.data.experience_id;
            
            const fileInput = document.getElementById('expFile');
            if (fileInput.files.length > 0) {
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                btn.textContent = 'Uploading file...';
                const uploadRes = await apiRequest(`/experiences/${expId}/upload`, {
                    method: 'POST',
                    body: formData,
                    isFormData: true
                });
                
                if (uploadRes.status !== 200 || !uploadRes.data.success) {
                    alert('Experience created, but file upload failed: ' + (uploadRes.data.message || ''));
                }
            }

            document.getElementById('createModal').close();
            e.target.reset();
            currentEditExpId = null;
            document.querySelector('#createModal h3').textContent = 'Ask a Query';
            loadExperiences();
        } else {
            let errorMsg = response.data.message || 'Failed to create experience';
            if (response.data.errors) {
                errorMsg += '\n' + Object.values(response.data.errors).join('\n');
            }
            alert(errorMsg);
        }

        btn.disabled = false;
        btn.textContent = 'Submit';
    });

    let searchTimeout;
    document.getElementById('searchInput').addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            currentSearch = e.target.value.trim();
            loadExperiences();
        }, 400);
    });

    document.addEventListener('DOMContentLoaded', loadExperiences);


</body>
</html>

let expList = [
    {
      "accepted_answer": "sure buddy",
      "author_id": 13,
      "author_name": "sahil",
      "category": "project",
      "company": "DYP",
      "content": "this is our CEP project",
      "created_at": "2026-08-26T11:42:08.939715",
      "experience_id": 10,
      "file_url": null,
      "is_resolved": true,
      "semester": "3rd",
      "tags": null,
      "title": "guys lets keep checking",
      "updated_at": "2026-08-26T19:12:29.827894",
      "views": 16
    }
];

let currentUserId = 13;
function formatHashtags(t) { return t; }

try {
    const rendered = expList.map(exp => `
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
                    ${exp.accepted_answer ? `
                    <div class="mt-2 p-4 bg-surface rounded-xl border border-secondary/20 flex gap-3 items-start" onclick="openExperienceDetail(${exp.experience_id}); event.stopPropagation();" style="cursor: pointer;">
                        <span class="material-symbols-outlined text-secondary">check_circle</span>
                        <div class="flex-1">
                            <p class="text-label-sm text-secondary font-bold mb-1">Accepted Answer</p>
                            <p class="text-body-md text-on-surface line-clamp-1">${exp.accepted_answer}</p>
                        </div>
                    </div>
                    ` : ''}
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
            console.log("Success!");
} catch (e) {
    console.error("Error:", e);
}

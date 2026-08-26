filepath = 'my_profile.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Profile Name
content = content.replace(
    '<h1 class="font-headline-md text-headline-md text-on-surface mb-1 relative z-10 user-name-display">Jordan Rivera</h1>',
    '<h1 id="profile-name" class="font-headline-md text-headline-md text-on-surface mb-1 relative z-10 user-name-display">Loading...</h1>'
)

# 2. Profile Role
content = content.replace(
    '<p class="font-label-md text-label-md text-primary bg-primary-fixed/50 px-3 py-1 rounded-full uppercase tracking-wider mb-4 relative z-10 user-role-display">Senior Student</p>',
    '<p id="profile-role" class="font-label-md text-label-md text-primary bg-primary-fixed/50 px-3 py-1 rounded-full uppercase tracking-wider mb-4 relative z-10 user-role-display">Loading...</p>'
)

# 3. Profile Bio
content = content.replace(
    '<p class="font-body-md text-body-md text-on-surface-variant mb-6 text-sm relative z-10">Computer Science major passionate about algorithmic problem solving and mentoring junior peers. Specializing in discrete mathematics and data structures.</p>',
    '<p id="profile-bio" class="font-body-md text-body-md text-on-surface-variant mb-6 text-sm relative z-10">Loading bio...</p>'
)

# 4. Message Button -> Edit Bio
old_buttons = """                            <div class="flex gap-2 w-full relative z-10">
                                <button class="flex-1 bg-primary text-on-primary font-label-md text-label-md py-2.5 rounded-lg shadow-sm hover:shadow-md transition-all flex items-center justify-center gap-2">
                                    <span class="material-symbols-outlined text-sm">message</span>
                                    Message
                                </button>
                                <button class="bg-surface-container-high text-on-surface p-2.5 rounded-lg hover:bg-surface-container-highest transition-colors flex items-center justify-center shadow-sm">
                                    <span class="material-symbols-outlined text-sm">more_horiz</span>
                                </button>
                            </div>"""

new_buttons = """                            <div class="flex gap-2 w-full relative z-10">
                                <button id="edit-bio-btn" class="flex-1 bg-primary text-on-primary font-label-md text-label-md py-2.5 rounded-lg shadow-sm hover:shadow-md transition-all flex items-center justify-center gap-2">
                                    <span class="material-symbols-outlined text-sm">edit</span>
                                    Edit Bio
                                </button>
                            </div>"""
content = content.replace(old_buttons, new_buttons)

# 5. Achievements block
old_achievements = """                        <!-- Badges & Achievements -->
                        <div class="bg-surface-container rounded-2xl p-6 shadow-sm flex flex-col gap-4">
                            <h3 class="font-headline-md text-label-md text-on-surface uppercase tracking-widest border-b border-outline-variant/30 pb-2">Achievements</h3>
                            <div class="flex flex-wrap gap-3">
                                <div class="flex items-center gap-2 bg-surface-container-high rounded-xl p-2 pr-4 shadow-sm hover:-translate-y-1 transition-transform cursor-default">
                                    <div class="w-8 h-8 rounded-full bg-secondary/10 flex items-center justify-center text-secondary">
                                        <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">workspace_premium</span>
                                    </div>
                                    <span class="font-label-md text-label-sm text-on-surface">Top Solver '24</span>
                                </div>
                                <div class="flex items-center gap-2 bg-surface-container-high rounded-xl p-2 pr-4 shadow-sm hover:-translate-y-1 transition-transform cursor-default">
                                    <div class="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                                        <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">psychology</span>
                                    </div>
                                    <span class="font-label-md text-label-sm text-on-surface">Master Mentor</span>
                                </div>
                                <div class="flex items-center gap-2 bg-surface-container-high rounded-xl p-2 pr-4 shadow-sm hover:-translate-y-1 transition-transform cursor-default">
                                    <div class="w-8 h-8 rounded-full bg-error-container text-on-error-container flex items-center justify-center">
                                        <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">local_fire_department</span>
                                    </div>
                                    <span class="font-label-md text-label-sm text-on-surface">100+ Streak</span>
                                </div>
                            </div>
                        </div>"""

new_achievements = """                        <!-- Badges & Achievements -->
                        <div class="bg-surface-container rounded-2xl p-6 shadow-sm flex flex-col gap-4">
                            <h3 class="font-headline-md text-label-md text-on-surface uppercase tracking-widest border-b border-outline-variant/30 pb-2">Achievements</h3>
                            <div id="achievements-container" class="flex flex-wrap gap-3">
                                <!-- Dynamic Achievements -->
                            </div>
                        </div>"""
content = content.replace(old_achievements, new_achievements)

# 6 & 7. Stats
content = content.replace(
    '<span class="font-display-lg text-headline-lg text-primary">342</span>',
    '<span id="stats-solved" class="font-display-lg text-headline-lg text-primary">0</span>'
)
content = content.replace(
    '<span class="font-display-lg text-headline-lg text-secondary">89</span>',
    '<span id="stats-helped" class="font-display-lg text-headline-lg text-secondary">0</span>'
)

# 8. Recent Solutions -> Recent Activity
content = content.replace('Recent Solutions', 'Recent Activity')
content = content.replace('id="recent-solutions-list"', 'id="recent-activity-list"')


with open(filepath, 'w') as f:
    f.write(content)
print("Done patching my_profile.html")

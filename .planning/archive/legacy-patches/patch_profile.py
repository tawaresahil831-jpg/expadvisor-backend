import re

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/my_profile.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Update Profile Picture UI to make it clickable and uploadable
# Find the image: <img alt="Profile" class="w-24 h-24 rounded-full object-cover border-4 border-surface shadow-md" src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&h=150&fit=crop" />
old_img_regex = r'<img alt="Profile" class="([^"]*)" src="([^"]*)" />'
new_img_html = """<label for="avatarUpload" class="cursor-pointer relative group block w-24 h-24 mx-auto">
                            <img alt="Profile" id="profileAvatarImg" class="\\1" src="\\2" />
                            <div class="absolute inset-0 bg-black/40 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                                <span class="material-symbols-outlined text-white text-xl">photo_camera</span>
                            </div>
                            <input type="file" id="avatarUpload" accept="image/*" class="hidden" onchange="uploadAvatar(event)">
                        </label>"""
content = re.sub(old_img_regex, new_img_html, content, count=1)

# 2. Add motivational quote to empty achievements
# The JS populates '#achievementsList'. It's currently in api.js or inline?
# Let's add it to the inline JS where populateUserProfile is called, or modify api.js if that's where it renders.
# Wait, my_profile.html doesn't have an inline renderAchievements. It relies on something else?

filepath = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/register.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Fix Username Field
bad_username_html = """                            <!-- Username (with error) -->
                            <div class="flex flex-col gap-1.5">
                                <label class="text-label-sm text-on-surface" style="color:#0b1c30;">Username</label>
                                <div class="relative">
                                    <input class="w-full px-4 py-3 rounded-xl bg-error-container/20 border border-error text-body-md text-on-surface focus:outline-none focus:border-error focus:ring-4 focus:ring-error/10 transition-all pr-10" style="background:rgba(255,218,214,0.2); border-color:#ba1a1a; color:#0b1c30;" type="text" id="username">
                                    <span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-error text-[20px]" style="color:#ba1a1a;">error</span>
                                </div>
                                <span class="text-label-sm text-error mt-0.5" style="color:#ba1a1a;"> </span>
                            </div>"""

good_username_html = """                            <!-- Username -->
                            <div class="flex flex-col gap-1.5">
                                <label class="text-label-sm text-on-surface" style="color:#0b1c30;">Username</label>
                                <input class="w-full px-4 py-3 rounded-xl bg-surface border border-outline-variant/50 text-body-md text-on-surface placeholder:text-on-surface-variant/50 focus:outline-none focus:border-secondary focus:ring-4 focus:ring-secondary/10 transition-all" style="background:#f8f9ff; border-color:rgba(197,198,205,0.5); color:#0b1c30;" placeholder="Enter your username" type="text" id="username">
                            </div>"""

content = content.replace(bad_username_html, good_username_html)

# 2. Fix Mobile Number Field
old_mobile_select = """                                    <select class="px-3 py-3 rounded-l-xl bg-surface border border-r-0 border-outline-variant/50 text-body-md text-on-surface focus:outline-none focus:border-secondary focus:ring-4 focus:ring-secondary/10 transition-all appearance-none cursor-pointer" style="background:#f8f9ff; border-color:rgba(197,198,205,0.5); color:#0b1c30;">
                                        <option>+1</option>
                                        <option>+44</option>
                                        <option>+91</option>
                                    </select>"""

new_mobile_select = """                                    <select disabled class="px-3 py-3 rounded-l-xl bg-surface border border-r-0 border-outline-variant/50 text-body-md text-on-surface focus:outline-none focus:border-secondary focus:ring-4 focus:ring-secondary/10 transition-all appearance-none" style="background:#f8f9ff; border-color:rgba(197,198,205,0.5); color:#0b1c30;">
                                        <option selected>+91</option>
                                    </select>"""

content = content.replace(old_mobile_select, new_mobile_select)

# Add maxlength="10" to tel input
content = content.replace('placeholder="Enter your mobile number" type="tel"', 'placeholder="Enter your mobile number" type="tel" maxlength="10" pattern="\\\\d{10}" oninput="this.value = this.value.replace(/[^0-9]/g, \'\');"')

with open(filepath, 'w') as f:
    f.write(content)

print("Done fixing fields")

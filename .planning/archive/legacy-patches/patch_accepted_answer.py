import re

# 1. Backend: app/models/experience.py
backend_file = '/Users/sahiltaware415/expadvisor-backend/app/models/experience.py'
with open(backend_file, 'r') as f:
    be_content = f.read()

to_dict_old = """    def to_dict(self):
        return {"""
to_dict_new = """    def to_dict(self):
        accepted_answer = None
        for c in self.comments:
            if getattr(c, 'is_accepted', False):
                accepted_answer = c.comment
                break

        return {
            "accepted_answer": accepted_answer,"""
be_content = be_content.replace(to_dict_old, to_dict_new)

with open(backend_file, 'w') as f:
    f.write(be_content)


# 2. Frontend: dashboard.html
frontend_file = '/Users/sahiltaware415/Documents/ExpAdvisor/expadvisor-frontend/frontend/dashboard.html'
with open(frontend_file, 'r') as f:
    fe_content = f.read()

card_render_old = """
                    <div class="flex flex-wrap gap-2">
                        <span class="px-2.5 py-1 rounded-md bg-surface-container-high text-on-surface-variant font-label-sm">${exp.category || 'General'}</span>
                        <span class="px-2.5 py-1 rounded-md border border-outline-variant/30 text-on-surface-variant font-label-sm">${exp.company || 'Company'}</span>
                    </div>
                    <div class="flex items-center justify-between pt-4 border-t border-outline-variant/10">"""

card_render_new = """
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
                    <div class="flex items-center justify-between pt-4 border-t border-outline-variant/10">"""

fe_content = fe_content.replace(card_render_old, card_render_new)

# Also check for Test data deletion script
del_script = """
import sys
sys.path.insert(0, '/Users/sahiltaware415/expadvisor-backend')
from app import create_app
from app.extensions import db
from app.models.experience import Experience

app = create_app()
with app.app_context():
    test_exps = Experience.query.filter(Experience.title.ilike('%Test Experience%')).all()
    for e in test_exps:
        db.session.delete(e)
    db.session.commit()
    print(f"Deleted {len(test_exps)} test experiences.")
"""
with open('del_test.py', 'w') as f:
    f.write(del_script)

with open(frontend_file, 'w') as f:
    f.write(fe_content)


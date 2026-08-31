# Technical Debt & Codebase Concerns

**Analysis Date:** 2026-08-31

## Areas of Concern & Technical Debt

### 1. Hardcoded Paths and External Directory References
- Multiple patch scripts at root (e.g. `patch_experience_model.py`, `patch_auth_google.py`) contain hardcoded absolute filesystem paths pointing outside this workspace (e.g. `/Users/sahiltaware415/expadvisor-backend/...`).
- A sibling directory `/Users/sahiltaware415/expadvisor-backend` exists outside the repository, while a local `backend/` directory also exists inside the workspace. The relation between these two backend copies needs consolidation or clear separation.

### 2. Ad-Hoc Patch Scripts Accumulation
- The workspace root and `expadvisor-frontend/` contain numerous `patch_*.py`, `fix_*.py`, and `temp_script*.js` files created during historical bug fixing and migrations.
- These scripts should be cleaned up or archived so they do not create confusion with the active production codebase.

### 3. Frontend Architecture Limitations
- The frontend is implemented as static HTML files with inline `<script>` tags and a shared `api.js`. As features grow, lack of a component architecture (e.g., React, Vue, or Web Components) leads to repeated HTML boilerplate across `dashboard.html`, `dashboard_v2.html`, `my_profile.html`, and `solve.html`.
- Use of the Tailwind CDN (`https://cdn.tailwindcss.com`) is recommended by Tailwind only for development/prototyping, not production, as it compiles CSS on the client side at runtime.

### 4. Git Repository Scope
- The workspace root (`/Users/sahiltaware415/Documents/ExpAdvisor`) was not initialized as a unified git repository, while subdirectories (`expadvisor-frontend/.git`, `expadvisor-frontend-test/.git`, and external `expadvisor-backend/.git`) contain individual git repositories. Initializing a root repository or managing submodules will ensure version tracking across the entire project.

### 5. Automated Unit & CI Testing Gaps
- Currently, test coverage relies strictly on `test_regression.py` running against a live backend server.
- Unit tests with mock databases (e.g. using `pytest` and SQLite in-memory) and GitHub Actions CI pipelines are absent.

*Concerns analysis: 2026-08-31*
<!-- refreshed: 2026-08-31 -->

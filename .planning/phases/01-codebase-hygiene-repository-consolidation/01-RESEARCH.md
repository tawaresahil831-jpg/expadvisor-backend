# Phase 1: Codebase Hygiene & Repository Consolidation - Research

**Researched:** 2026-08-31
**Domain:** Monorepo consolidation, legacy script cleanup, Python backend alignment, Git repository unification
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

No user constraints - all decisions at agent discretion.

### Scope Fences
- Focus strictly on hygiene: consolidating backend code, removing obsolete patch scripts, and establishing a unified workspace structure.
- Do NOT make breaking changes to existing database schema or API endpoint signatures.
- Preserve all active HTML pages (`expadvisor-frontend/frontend/`) and core backend logic (`routes/`, `models/`, `utils/`).
</user_constraints>

<architectural_responsibility_map>
## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Backend Alignment | API/Backend | File System | Synchronize missing models, routes, and `run.py` from external `expadvisor-backend` into local `backend/` |
| Legacy Script Cleanup | Dev/Tooling | File System | Archive or delete ~30 ad-hoc `patch_*.py` and `temp_script*.js` files scattered across root and frontend |
| Git Unification | Dev/Tooling | VCS | Decide and establish clean Git tracking (root repo vs submodules/remotes) without nested repo collision |

</architectural_responsibility_map>

<research_summary>
## Summary

Investigation revealed that the current workspace (`/Users/sahiltaware415/Documents/ExpAdvisor`) contains:
1. An incomplete local `backend/app/` missing `app/models/`, `app/routes/like.py`, `app/routes/notification.py`, `app/routes/user.py`, `run.py`, and `requirements.txt`.
2. The active, complete backend actually resides at `/Users/sahiltaware415/expadvisor-backend`, and all ad-hoc patch scripts in `ExpAdvisor` contain hardcoded paths pointing to that directory.
3. `ExpAdvisor` has over 35 temporary Python patch scripts (`patch_*.py`, `fix_*.py`) and JavaScript dump files (`temp_script*.js`) that were executed once to hot-patch files and are now dead code.
4. There are multiple conflicting Git histories: `expadvisor-frontend/.git`, `expadvisor-frontend-test/.git`, and external `/Users/sahiltaware415/expadvisor-backend/.git`, while the workspace root has no git initialized.

### Recommended Strategy
1. **Consolidate Backend (HYG-01):**
   - Copy missing models (`app/models/`), routes (`like.py`, `notification.py`, `user.py`), utils (`email_utils.py`), and root files (`run.py`, `requirements.txt`, `Procfile`) from `/Users/sahiltaware415/expadvisor-backend` directly into `backend/`.
   - Update any configuration/paths so `backend/` is 100% self-contained and runnable from within `ExpAdvisor`.
2. **Archive/Purge Ad-Hoc Scripts (HYG-02):**
   - Create an `archive/legacy-patches/` directory or safely remove verified obsolete patch scripts (`patch_*.py`, `fix_*.py`, `temp_script*.js`) from root and frontend.
   - Clean up `check_db.py`, `del_test.py` from frontend root.
3. **Repository Consolidation (HYG-03):**
   - Ensure `backend/` and `frontend/` have clear `.gitignore` files ignoring `.env`, `venv/`, `__pycache__`, and IDE files.
   - Clean up test/redundant folders like `expadvisor-frontend-test` or archive them.
   - Initialize a unified root Git repository or organize remotes cleanly so the entire monorepo is version-tracked together.

### Verification Strategy
- Execute `test_regression.py` against the local consolidated backend to guarantee zero regressions.
- Verify `grep -rn "expadvisor-backend" .` returns zero matches in active source files.
- Verify clean `git status` at root.
</research_summary>

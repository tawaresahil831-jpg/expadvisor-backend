---
phase: "1"
slug: "codebase-hygiene-repository-consolidation"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-08-31"
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python standard library & `requests` |
| **Config file** | `backend/app/config.py` & `.env` |
| **Quick run command** | `grep -rn "expadvisor-backend" backend/ expadvisor-frontend/frontend/ 2>/dev/null || echo "CLEAN"` |
| **Full suite command** | `python3 test_regression.py` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run quick check for external hardcoded paths
- **After every plan wave:** Run `python3 test_regression.py` against the consolidated backend
- **Before `/gsd-verify-work`:** Full regression suite green and clean git status

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | HYG-01 | Self-contained backend without external path leaks | sanity | `python3 -c "import app; print('Backend imports OK')"` | ✅ | ⬜ pending |
| 01-01-02 | 01 | 1 | HYG-01 | Backend routes and models run correctly | integration | `python3 test_regression.py` | ✅ | ⬜ pending |
| 01-02-01 | 02 | 2 | HYG-02 | Dead patch scripts removed safely | check | `ls patch_*.py 2>/dev/null \| wc -l` | ✅ | ⬜ pending |
| 01-02-02 | 02 | 2 | HYG-03 | Unified root git repository initialized with proper .gitignore | vcs | `git status` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---
phase: "2"
slug: "automated-testing-infrastructure"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-08-31"
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Pytest 8.x |
| **Config file** | `backend/pytest.ini` / `backend/tests/conftest.py` |
| **Quick run command** | `backend/venv/bin/pytest backend/tests/test_auth.py` |
| **Full suite command** | `backend/venv/bin/pytest backend/tests` |
| **Estimated runtime** | ~3 seconds |

---

## Sampling Rate

- **After every task commit:** Run quick test on targeted file
- **After every plan wave:** Run `backend/venv/bin/pytest backend/tests`
- **Before `/gsd-verify-work`:** Full suite must pass with 100% green tests

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | TEST-01 | Test config with in-memory SQLite and disabled limiter | unit | `backend/venv/bin/python -c "from app.config import TestConfig; print(TestConfig.TESTING)"` | ❌ W0 | ⬜ pending |
| 02-01-02 | 01 | 1 | TEST-01 | In-memory DB and test client fixtures load cleanly | fixture | `backend/venv/bin/pytest backend/tests -v` | ❌ W0 | ⬜ pending |
| 02-01-03 | 01 | 1 | TEST-01 | Auth, experience, comment & like unit tests pass | integration | `backend/venv/bin/pytest backend/tests` | ❌ W0 | ⬜ pending |
| 02-02-01 | 02 | 2 | TEST-02 | GitHub Actions CI workflow runs lint and pytest | ci | `test -f .github/workflows/ci.yml` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

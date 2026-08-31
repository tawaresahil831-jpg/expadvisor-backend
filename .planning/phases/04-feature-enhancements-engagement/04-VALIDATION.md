---
phase: "4"
slug: "feature-enhancements-engagement"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-08-31"
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Pytest 8.x & Browser Verification |
| **Config file** | `backend/pytest.ini` & `expadvisor-frontend/frontend/js/api.js` |
| **Quick run command** | `backend/venv/bin/pytest backend/tests/test_notifications_bookmarks.py` |
| **Full suite command** | `backend/venv/bin/pytest backend/tests` |
| **Estimated runtime** | ~6 seconds |

---

## Sampling Rate

- **After every task commit:** Run quick test suite on notifications and bookmarks
- **After every plan wave:** Run full pytest suite across backend
- **Before `/gsd-verify-work`:** All backend tests green and UI notification badge responsive

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | ENG-01 | Notification unread count and mark-as-read endpoints | unit | `backend/venv/bin/pytest backend/tests/test_notifications_bookmarks.py` | ❌ W0 | ⬜ pending |
| 04-01-02 | 01 | 1 | ENG-01 | Client header notification badge integration | ui | `grep -rn "updateNotificationBadge" expadvisor-frontend/frontend/js/api.js` | ❌ W0 | ⬜ pending |
| 04-02-01 | 02 | 2 | ENG-02 | Bookmark model, routes, and tests | integration | `backend/venv/bin/pytest backend/tests` | ❌ W0 | ⬜ pending |
| 04-02-02 | 02 | 2 | ENG-03 | Feed multi-filtering and client bookmark toggling | ui | `grep -rn "toggleBookmark" expadvisor-frontend/frontend/js/api.js` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

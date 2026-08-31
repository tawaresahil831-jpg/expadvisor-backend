---
phase: "3"
slug: "frontend-build-asset-modernization"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-08-31"
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Tailwind CSS CLI / NPM scripts & Static HTTP Server |
| **Config file** | `expadvisor-frontend/package.json` & `expadvisor-frontend/tailwind.config.js` |
| **Quick run command** | `test -f expadvisor-frontend/frontend/css/output.css` |
| **Full suite command** | `npm --prefix expadvisor-frontend run build:css` |
| **Estimated runtime** | ~2 seconds |

---

## Sampling Rate

- **After every task commit:** Run build check and verify compiled CSS exists
- **After every plan wave:** Check page rendering with pre-compiled CSS bundle
- **Before `/gsd-verify-work`:** Full build runs with 0 errors and zero dead links

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | FE-01 | Tailwind build compiles static CSS asset | build | `npm --prefix expadvisor-frontend run build:css` | ❌ W0 | ⬜ pending |
| 03-01-02 | 01 | 1 | FE-01 | Precompiled stylesheet linked in HTML pages | layout | `grep -rn "output.css" expadvisor-frontend/frontend/*.html` | ❌ W0 | ⬜ pending |
| 03-02-01 | 02 | 2 | FE-02 | Centralized navigation & modal helper scripts | ui | `test -f expadvisor-frontend/frontend/js/ui-layout.js` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

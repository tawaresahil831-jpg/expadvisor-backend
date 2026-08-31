# Roadmap: ExpAdvisor

## Overview

ExpAdvisor has an existing, functional core featuring user authentication, experience publishing, threaded comments with accepted answers, and file uploads. The brownfield roadmap organizes technical consolidation, automated test infrastructure, and frontend production hardening to transition ExpAdvisor into a robust, maintainable product.

## Phases

- [x] **Phase 1: Codebase Hygiene & Repository Consolidation** - Clean up ad-hoc patch scripts, eliminate external hardcoded paths, and unify git tracking.
- [x] **Phase 2: Automated Testing Infrastructure** - Implement isolated pytest test suites with test DB fixtures, deprecating script-only regression checks.
- [x] **Phase 3: Frontend Build & Asset Modernization** - Replace client-side Tailwind CDN with an optimized build system and clean up repetitive template code.
- [x] **Phase 4: Feature Enhancements & Engagement** - Expand notification workflows, user bookmarks, and advanced search filters.

## Phase Details

### Phase 1: Codebase Hygiene & Repository Consolidation
**Goal**: Remove technical debt from ad-hoc patching scripts and ensure the workspace is self-contained with unified version control.
**Depends on**: Nothing
**Requirements**: [HYG-01, HYG-02, HYG-03]
**Success Criteria**:
  1. No scripts reference outside hardcoded filesystem paths (`/Users/sahiltaware415/expadvisor-backend`).
  2. Root directory is clean of single-use migration/patch scripts.
  3. Single git repository manages the complete codebase.
**Plans**: 2 plans

Plans:
- [x] 01-01: Synchronize missing models, routes, runner from expadvisor-backend into backend/ and eliminate external path references
- [x] 01-02: Purge ad-hoc patch scripts, clean up test clones, and establish unified root Git tracking

### Phase 2: Automated Testing Infrastructure
**Goal**: Provide fast, reliable automated test coverage for Flask API routes and model validation.
**Depends on**: Phase 1
**Requirements**: [TEST-01, TEST-02]
**Success Criteria**:
  1. `pytest` runs locally without requiring an active external database server.
  2. Authentication, experience CRUD, comment, and like flows pass unit and integration tests.
**Plans**: 2 plans

Plans:
- [x] 02-01: Implement in-memory SQLite fixtures and pytest test suites for Auth, Experiences, Comments, and Likes
- [x] 02-02: Configure GitHub Actions CI workflow to run test suite on pushes and pull requests

### Phase 3: Frontend Build & Asset Modernization
**Goal**: Transition static HTML pages to a consistent UI architecture with compiled styling.
**Depends on**: Phase 1
**Requirements**: [FE-01, FE-02]
**Success Criteria**:
  1. Production bundle eliminates CDN compilation lag.
  2. Shared components (header, sidebar, user badge) are DRY and centrally updated.
**Plans**: 2 plans

Plans:
- [x] 03-01: Setup Tailwind CLI build process, compile minified output.css, and integrate into HTML pages
- [x] 03-02: Implement shared ui-layout.js for navigation, drawer menus, and modal dialogs

### Phase 4: Feature Enhancements & Engagement
**Goal**: Elevate community engagement with unread notification workflows and multi-filter discovery.
**Depends on**: Phase 3
**Requirements**: [ENG-01, ENG-02, ENG-03]
**Success Criteria**:
  1. Live notification badge counter and mark-as-read integration in UI header.
  2. Experience bookmarks API and client-side saved list.
  3. Search and category/company multi-filtering across feed views.
**Plans**: 2 plans

Plans:
- [x] 04-01: Notification badge count, mark-read integration, and notification unit tests
- [x] 04-02: Bookmarks/Saved experiences API and client feed filtering

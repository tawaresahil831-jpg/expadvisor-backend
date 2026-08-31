# Roadmap: ExpAdvisor

## Overview

ExpAdvisor has an existing, functional core featuring user authentication, experience publishing, threaded comments with accepted answers, and file uploads. The brownfield roadmap organizes technical consolidation, automated test infrastructure, and frontend production hardening to transition ExpAdvisor into a robust, maintainable product.

## Phases

- [x] **Phase 1: Codebase Hygiene & Repository Consolidation** - Clean up ad-hoc patch scripts, eliminate external hardcoded paths, and unify git tracking.
- [ ] **Phase 2: Automated Testing Infrastructure** - Implement isolated pytest test suites with test DB fixtures, deprecating script-only regression checks.
- [ ] **Phase 3: Frontend Build & Asset Modernization** - Replace client-side Tailwind CDN with an optimized build system and clean up repetitive template code.
- [ ] **Phase 4: Feature Enhancements & Engagement** - Expand notification workflows, user bookmarks, and advanced search filters.

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
**Plans**: TBD

### Phase 3: Frontend Build & Asset Modernization
**Goal**: Transition static HTML pages to a consistent UI architecture with compiled styling.
**Depends on**: Phase 1
**Requirements**: [FE-01, FE-02]
**Success Criteria**:
  1. Production bundle eliminates CDN compilation lag.
  2. Shared components (header, sidebar, user badge) are DRY and centrally updated.
**Plans**: TBD

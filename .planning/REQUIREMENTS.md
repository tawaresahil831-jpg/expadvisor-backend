# Requirements: ExpAdvisor

**Defined:** 2026-08-31
**Core Value:** Empowering students with peer-sourced, authentic interview and career experience insights to make informed academic and professional decisions.

## Existing & Validated Requirements

### Authentication & User Management
- [x] **AUTH-01**: Student registration with name, email, password, college, branch, year.
- [x] **AUTH-02**: Login with email and password returning JWT token.
- [x] **AUTH-03**: Social authentication via Google OAuth.
- [x] **AUTH-04**: Current user endpoint (`GET /api/auth/me`) with token validation.
- [x] **AUTH-05**: Profile updates with avatar upload.

### Experiences & Feeds
- [x] **EXP-01**: Create experience posts with title, content, category, semester, company.
- [x] **EXP-02**: List experiences with pagination, search, and category/company filtering.
- [x] **EXP-03**: Single experience detail view with view count incrementing.
- [x] **EXP-04**: Update and delete experience with author ownership enforcement.
- [x] **EXP-05**: Multipart file attachment support via Supabase object storage.

### Social Interaction & Solving
- [x] **SOC-01**: Threaded commenting under experience posts.
- [x] **SOC-02**: Mark comment as accepted solution ("solve" flow).
- [x] **SOC-03**: Toggle like/upvote on experiences with live counter.
- [x] **SOC-04**: Student directory for networking and connecting with peers.

## Brownfield Stabilization & Next Phase Requirements

### Codebase Hygiene & Consolidation
- [x] **HYG-01**: Consolidate backend source files and remove hardcoded absolute paths pointing to external `/Users/sahiltaware415/expadvisor-backend`.
- [x] **HYG-02**: Clean up obsolete `patch_*.py` and `temp_script*.js` files from root and frontend.
- [x] **HYG-03**: Initialize unified root git repository covering backend and frontend codebases.

### Quality Assurance & Automated Testing
- [x] **TEST-01**: Establish unit and integration test suite using `pytest` with in-memory SQLite/Postgres test fixtures.
- [x] **TEST-02**: Setup continuous integration workflow (GitHub Actions).

### Frontend Production Hardening
- [x] **FE-01**: Eliminate runtime Tailwind CDN script in favor of a modern build or pre-compiled bundle.
- [x] **FE-02**: Standardize shared navigation, headers, and modals across all HTML pages.

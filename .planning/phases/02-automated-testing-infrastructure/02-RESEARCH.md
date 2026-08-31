# Phase 2: Automated Testing Infrastructure - Research

**Researched:** 2026-08-31
**Domain:** Python testing with Pytest, Flask test client fixtures, SQLite in-memory test databases, GitHub Actions CI
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

No user constraints - all decisions at agent discretion.

### Scope Fences
- Tests must run standalone without requiring network access or connection to the remote Supabase PostgreSQL database.
- CI pipeline must run on push and pull requests on GitHub Actions.
- Preserve existing application behavior and avoid modifying production database state during test execution.
</user_constraints>

<architectural_responsibility_map>
## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Test Configuration | API/Backend | File System | Define `TestConfig` with `TESTING=True`, `SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"`, and disabled rate limiting |
| Pytest Fixtures | API/Backend | Dev/Tooling | Provide `conftest.py` with `app`, `client`, `db_session`, `auth_headers` fixtures |
| Unit & Route Tests | API/Backend | Test Suite | Test auth flows, experience CRUD, comment discussions, and likes using Flask's `client` |
| CI Pipeline | Dev/Tooling | GitHub Actions | Setup `.github/workflows/ci.yml` running lint and pytest on push and PR |

</architectural_responsibility_map>

<research_summary>
## Summary

### Current State
Currently, ExpAdvisor has only `test_regression.py`, which is an integration script requiring an active Flask server running on port 5001 connected to the live Supabase PostgreSQL database. There are no automated unit tests, no test fixtures, and no continuous integration.

### Proposed Architecture for Automated Testing
1. **Application Factory Modification:**
   - Update `create_app(config_class=Config)` in `backend/app/__init__.py` to accept an optional configuration class or dictionary, allowing `TestConfig` to be injected cleanly.
   - Support `TESTING=True` to disable rate limiting (`limiter.enabled = False`) during test runs to prevent 429 errors.
2. **Test Fixtures (`backend/tests/conftest.py`):**
   - Provide an in-memory SQLite database (`sqlite:///:memory:`) that creates all tables per test session or test function and drops them after teardown.
   - Provide a fixture for authenticated client headers (`auth_headers`) by creating a verified mock test user and generating a valid JWT token.
3. **Core Test Suites (`backend/tests/`):**
   - `test_auth.py`: Registration with validation, duplicate email prevention, OTP verification, and login.
   - `test_experiences.py`: Creation, fetching, pagination, updating, deleting, and ownership protection.
   - `test_comments_likes.py`: Commenting, marking accepted answers, and toggling likes.
4. **Continuous Integration (`.github/workflows/ci.yml`):**
   - GitHub Actions workflow running on Ubuntu with Python 3.10/3.11.
   - Installs dependencies from `backend/requirements.txt` plus `pytest`.
   - Executes `pytest backend/tests` automatically on every push or pull request.
</research_summary>

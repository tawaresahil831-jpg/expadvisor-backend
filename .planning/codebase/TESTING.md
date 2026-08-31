# Testing Strategy & Verification

**Analysis Date:** 2026-08-31

## Testing Overview

ExpAdvisor currently uses an end-to-end integration test runner (`test_regression.py`) rather than isolated unit tests with mock databases. The regression script tests live HTTP endpoints against a running backend instance.

## Test Structure

### Integration Regression Suite (`test_regression.py`)
- **Target:** Live running Flask instance at `http://127.0.0.1:5001/api`.
- **Driver:** Python `requests` library with persistent session state (`requests.Session()`).
- **Execution:**
  ```bash
  python3 test_regression.py
  ```
- **Flow Tested:**
  1. **User Registration:** Creates an ephemeral test user account (`test_<uuid>@example.com`).
  2. **Authentication / Login:** Obtains JWT token and attaches `Authorization: Bearer <token>` to session headers.
  3. **Experience Lifecycle:**
     - Create experience post (`POST /experiences`)
     - Retrieve single experience (`GET /experiences/<id>`)
     - Query and paginate experiences (`GET /experiences?page=1&per_page=5&search=Test`)
     - Update experience post (`PUT /experiences/<id>`)
     - Upload file attachment (`POST /experiences/<id>/upload` with multipart dummy PDF)
  4. **Social & Discussion:**
     - Add comment (`POST /experiences/<id>/comments`)
     - Fetch comments list (`GET /experiences/<id>/comments`)
     - Delete comment (`DELETE /comments/<id>`)
     - Add like/upvote (`POST /experiences/<id>/like`)
     - Verify like count (`GET /experiences/<id>/likes`)
     - Remove like (`DELETE /experiences/<id>/like`)
  5. **Cleanup:**
     - Deletes the test experience post (`DELETE /experiences/<id>`).

## Manual Verification Patterns

- Frontend manual verification can be performed using local HTTP servers (e.g. `python3 -m http.server` inside `expadvisor-frontend/frontend/`) or via Vercel preview URLs.
- Cross-browser checks for Tailwind CDN rendering and responsiveness across desktop and mobile viewports.

*Testing analysis: 2026-08-31*
<!-- refreshed: 2026-08-31 -->

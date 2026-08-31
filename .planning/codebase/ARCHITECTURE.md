# System Architecture

**Analysis Date:** 2026-08-31

## Architectural Pattern

ExpAdvisor implements a decoupled **Client-Server Architecture** consisting of:
1. **RESTful API Backend:** A stateless Flask web service exposing JSON endpoints for data persistence, authentication, and file storage.
2. **Static Multi-Page Application (MPA) Frontend:** Pure HTML5 pages styled with Tailwind CSS, using client-side JavaScript (`fetch`) to interact with the backend API.

```
       +-------------------------------------------------------------+
       |                  ExpAdvisor Frontend                        |
       |  (Static HTML/Tailwind MPA hosted on Vercel)                |
       |  dashboard.html, login.html, solve.html, my_profile.html    |
       +------------------------------+------------------------------+
                                      |
                           HTTPS REST Requests
                           (Bearer JWT Token)
                                      v
       +-------------------------------------------------------------+
       |                  ExpAdvisor Flask Backend                   |
       |  (Python Flask WSGI App hosted on Render)                   |
       |  - Flask Blueprints: auth, experience, comment, like, upload|
       |  - Security: Flask-Limiter, Werkzeug hashing, JWT           |
       |  - ORM: Flask-SQLAlchemy (PostgreSQL)                       |
       +--------------+------------------------------+---------------+
                      |                              |
            SQLAlchemy (psycopg2)              Supabase Storage SDK
                      v                              v
       +-----------------------------+ +-----------------------------+
       |   PostgreSQL Database       | |  Supabase Object Storage    |
       |   (Supabase / Remote DB)    | |  (Uploaded PDFs, Avatars)   |
       +-----------------------------+ +-----------------------------+
```

## Backend Architecture

### Application Factory Pattern
- The backend uses Flask's application factory (`create_app()` in `backend/app/__init__.py`).
- Configuration is loaded from `app.config.Config` using environment variables.
- Extensions (`db`, `limiter`, `cors`) are instantiated centrally in `app.extensions` and bound to the app instance in `create_app()`.

### Blueprints (Modular Routing)
- `auth_bp` (`/api/auth`): Handles registration, credentials login, Google OAuth, and current user profile fetching (`/api/auth/me`).
- `experience_bp` (`/api/experiences`): Manages full lifecycle of experiences/posts (CRUD, search, filtering by category/company, view counting, pagination).
- `comment_bp` (`/api/experiences/<id>/comments` & `/api/comments/<id>`): Threaded comments, deletion, and marking accepted answers.
- `like_bp` (`/api/experiences/<id>/like`): Toggling upvotes/likes with counter updates.
- `upload_bp` (`/api/experiences/<id>/upload`): Handles multipart file attachments via Supabase.
- `admin_bp` (`/api/admin`): Administrative maintenance and user management.

### Authentication & Authorization
- Token-based stateless authentication using JWT.
- `@token_required` decorator wraps protected view functions, validates `Bearer` tokens, and injects `current_user` into route handlers.
- Ownership checks: Write and delete operations verify that `current_user.id == resource.user_id`.

## Frontend Architecture

### Multi-Page Application (MPA)
- Distinct HTML pages for separate domains:
  - `login.html` / `register.html` / `forgot_pass.html` / `reset_password.html`: Authentication flows.
  - `dashboard.html` / `dashboard_v2.html`: Main community experience feed, search, and category exploration.
  - `solve.html`: Question & answer problem-solving workflow.
  - `my_profile.html`: User profile overview, stats, and personal posts.
  - `my_problems.html`: User's authored questions/posts and status tracking.
  - `student_directory.html`: Peer directory and network discovery.
- Shared communication layer: `frontend/js/api.js` encapsulates `apiRequest()`, JWT token lifecycle management (`getToken`, `setToken`, `removeToken`), auto-redirection on 401 Unauthorized, and dynamic DOM profile population (`populateUserProfile`).

*System architecture analysis: 2026-08-31*
<!-- refreshed: 2026-08-31 -->

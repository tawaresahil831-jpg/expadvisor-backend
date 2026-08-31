# Directory & Codebase Structure

**Analysis Date:** 2026-08-31

## Repository Layout

The workspace root `/Users/sahiltaware415/Documents/ExpAdvisor` contains the backend source, frontend UI assets, standalone migration/patch utilities, and test suites.

```
ExpAdvisor/
├── .env                              # Environment variable configuration for backend
├── .planning/                        # GSD system planning and codebase documentation
│   └── codebase/                     # Evidence-backed codebase intelligence documents
├── backend/                          # Backend Flask microservice codebase
│   ├── README.md                     # Backend API documentation and endpoint specification
│   └── app/                          # Flask application package
│       ├── __init__.py               # Flask app factory (`create_app`)
│       ├── config.py                 # Application configuration and environment mappings
│       ├── extensions.py             # Instantiation of db (SQLAlchemy) & limiter
│       ├── routes/                   # Blueprint definitions for API endpoints
│       │   ├── auth.py               # /api/auth routes (register, login, me)
│       │   ├── experience.py         # /api/experiences CRUD, pagination, filtering
│       │   ├── comment.py            # /api/comments routes & comment discussions
│       │   ├── upload.py             # /api/experiences/<id>/upload file attachments
│       │   └── admin.py              # /api/admin maintenance and management
│       └── utils/                    # Shared backend helpers
│           ├── auth_utils.py         # `@token_required` decorator and JWT verification
│           └── validators.py         # Input validation routines (length, enum, format)
├── expadvisor-frontend/              # Production frontend multi-page static site
│   ├── vercel.json                   # Vercel routing configuration
│   ├── index.html                    # Entry redirection to frontend dashboard
│   ├── frontend/                     # Core HTML pages and client assets
│   │   ├── dashboard.html            # Main feed & experience browsing interface
│   │   ├── dashboard_v2.html         # Alternative/experimental dashboard layout
│   │   ├── login.html                # Student login page
│   │   ├── register.html             # Student account registration
│   │   ├── forgot_pass.html          # Password reset request page
│   │   ├── reset_password.html       # Password reset confirmation
│   │   ├── check_mail.html           # Email confirmation notice
│   │   ├── my_profile.html           # Profile view and editor
│   │   ├── my_problems.html          # User's posted problems and solutions
│   │   ├── solve.html                # Problem solving & discussion page
│   │   ├── student_directory.html    # Directory of registered students
│   │   ├── js/
│   │   │   └── api.js                # Core API client and auth helper functions
│   │   └── vercel.json               # Static rewrite rules
│   └── [patch_*.py, fix_*.py]        # Historic utility scripts for UI/data modifications
├── expadvisor-frontend-test/         # Test/backup sandbox mirror of frontend assets
├── patch_*.py                        # Root database/model patching scripts
└── test_regression.py                # End-to-end integration test runner
```

## Key File Locations & Responsibilities

| Path | Purpose |
|------|---------|
| `backend/app/__init__.py` | Creates and configures Flask application instance and registers all route blueprints |
| `backend/app/routes/experience.py` | Core domain logic for experiences, filtering, searching, and pagination |
| `backend/app/utils/auth_utils.py` | JWT extraction, decoding, and user session injection |
| `expadvisor-frontend/frontend/js/api.js` | Central frontend HTTP client with auth token management and 401 handling |
| `expadvisor-frontend/frontend/dashboard.html` | Primary community landing and interaction view |
| `test_regression.py` | Comprehensive live regression testing script checking end-to-end API workflows |

*Structure analysis: 2026-08-31*
<!-- refreshed: 2026-08-31 -->

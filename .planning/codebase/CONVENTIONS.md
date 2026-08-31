# Code Conventions & Style

**Analysis Date:** 2026-08-31

## Backend Conventions (Python / Flask)

### API Response Format
All Flask endpoints return a standardized JSON envelope structure:
```json
{
  "success": true,
  "message": "Human readable status message",
  "data": { ... }
}
```
For error states (e.g. 400 Bad Request):
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "field_name": "Error explanation"
  }
}
```
For paginated responses:
```json
{
  "success": true,
  "message": "Experiences fetched successfully",
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_items": 42,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

### Route & Controller Patterns
- Route blueprints defined per domain (`auth_bp`, `experience_bp`, `comment_bp`, etc.) with explicit URL prefixes (`/api/auth`, `/api/experiences`).
- Decorators used for authorization (`@token_required`) and rate limiting (`@limiter.limit("5 per minute")`).
- Input extraction prefers `request.get_json(silent=True) or {}` to avoid throwing uncaught JSON decode exceptions.
- Input validation handled via helper functions in `app.utils.validators` (`validate_length`, `validate_email`, `validate_choice`, `validate_semester`).

### Database Model Standards
- SQLAlchemy models define a `to_dict()` serialization method returning primitive dictionaries suitable for `jsonify`.
- Passwords are never stored in plain text; handled via `set_password(password)` and `check_password(password)` wrapping `werkzeug.security.generate_password_hash` and `check_password_hash`.
- Foreign key cascading is respected for child entities (e.g. comments and likes belong to experiences/users).

## Frontend Conventions (JavaScript / HTML)

### Client API Invocation
- All network interaction is routed through `apiRequest(endpoint, options)` in `expadvisor-frontend/frontend/js/api.js`.
- JWT token is managed using helper functions: `getToken()`, `setToken(token)`, and `removeToken()`.
- HTTP 401 handling is global: automatically clears the stored token and redirects the browser to `login.html`.
- Protected views invoke `requireAuth()` immediately upon script evaluation.

### Styling & Markup Conventions
- Utility-first styling with Tailwind CSS via CDN script with customized color tokens (`brand`, `surface`, `canvas`).
- Icons use Google Material Symbols Outlined (`<span class="material-symbols-outlined">icon_name</span>`).
- Reusable UI elements (profile header, badges, navigation sidebar) follow consistent DOM class naming patterns.

*Conventions analysis: 2026-08-31*
<!-- refreshed: 2026-08-31 -->

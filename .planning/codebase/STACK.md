# Technology Stack

**Analysis Date:** 2026-08-31

## Languages

**Primary:**
- Python 3.10+ - Backend API service (`backend/app/`, `patch_*.py` migration/patching scripts)
- JavaScript (ES6+) - Frontend client-side business logic and DOM manipulation (`expadvisor-frontend/frontend/js/api.js`, inline scripts)
- HTML5 / CSS3 - Multi-page web layout and styling (`expadvisor-frontend/frontend/*.html`)

## Runtime

**Environment:**
- Python 3 (`python3`) with Flask WSGI server (Gunicorn for production on Render)
- Modern Web Browsers (Chrome, Firefox, Safari, Edge) executing vanilla JavaScript

**Package Manager:**
- Python `pip` with `requirements.txt` (dependencies in root/backend virtual environment)
- CDN-based frontend distribution (no Node.js/npm build pipeline; Tailwind CSS loaded via CDN)

## Frameworks

**Core:**
- Flask 3.0.3 - Lightweight Python WSGI web application framework
- Flask-SQLAlchemy 3.1.1 & SQLAlchemy 2.0.51 - ORM and database abstraction layer
- Flask-Limiter - Rate limiting for authentication and API endpoints
- Flask-CORS - Cross-Origin Resource Sharing handling for frontend-backend communication
- Tailwind CSS (CDN Play / Script tag) - Utility-first CSS styling on the frontend

**Testing:**
- Python standard library & `requests` - Integration regression test suite (`test_regression.py`)

## Key Dependencies

**Backend:**
- `PyJWT==2.9.0` - Authentication token signing and verification
- `Werkzeug==3.1.8` - Password hashing and secure filename utilities
- `psycopg2-binary==2.9.12` - PostgreSQL database adapter
- `supabase==2.10.0` - Supabase Storage and database client integration
- `python-dotenv==1.0.1` - Environment variable loading from `.env`
- `google-auth` - Google OAuth authentication support
- `gunicorn` - Production WSGI server

**Frontend:**
- Google Fonts (`Inter`) & Google Material Symbols Outlined
- Tailwind CSS CDN script
- Vanilla Fetch API for asynchronous HTTP communication

## Configuration

- Backend environment variables loaded via `.env`:
  - `DATABASE_URL` - PostgreSQL database connection URI
  - `SECRET_KEY` - Flask session secret
  - `JWT_SECRET_KEY` - Token signing key
  - `SUPABASE_URL` - Supabase project URL
  - `SUPABASE_KEY` - Supabase API key
  - `FLASK_ENV` - Environment control (debug vs production)
- Vercel Deployment Configuration (`vercel.json` in `expadvisor-frontend/`):
  - Rewrites and clean URL configuration for static frontend hosting on Vercel
- Render Deployment Configuration (`Procfile`):
  - `web: gunicorn run:app`

*Technology stack analysis: 2026-08-31*
<!-- refreshed: 2026-08-31 -->

# Integrations & External Services

**Analysis Date:** 2026-08-31

## Databases & Storage

### PostgreSQL (Supabase / Managed DB)
- **Role:** Primary relational data store for all user profiles, experiences/articles, comments, likes, and notifications.
- **Client/Driver:** `SQLAlchemy` ORM via `psycopg2-binary`.
- **Connection URI:** Supplied via `DATABASE_URL` in `.env`.
- **Key Tables:**
  - `users` - User credentials, profile info, avatar URL, college, branch, graduation year, role.
  - `experiences` - Postings/stories/problems with category, company, semester, file attachment URLs, view counts, resolved status.
  - `comments` - Discussions on experiences, with accepted answer flags.
  - `likes` - User upvotes/likes on experiences.
  - `notifications` - Alerts for upvotes, comments, and accepted answers.

### Supabase Storage
- **Role:** Cloud object storage for media attachments and avatars.
- **Client:** `supabase` Python SDK (`supabase==2.10.0`).
- **Configuration:** `SUPABASE_URL` and `SUPABASE_KEY` credentials in backend environment.
- **Upload Endpoints:**
  - `/api/experiences/<id>/upload` - Attachment uploads for experiences (PDFs, images).
  - Avatar uploads for user profiles.

## Authentication & Identity

### JWT (JSON Web Tokens)
- **Role:** Stateless session tokens for client authentication.
- **Library:** `PyJWT`.
- **Mechanism:** Bearer token transmitted in HTTP `Authorization` header (`Authorization: Bearer <token>`).
- **Client Storage:** Stored in browser `localStorage` under `expadvisor_token`.

### Google OAuth (Sign-In with Google)
- **Role:** Social authentication option for fast student sign-in.
- **Library:** `google-auth` on backend; Google Identity Services on frontend.
- **Endpoints:** Handled via Google token verification endpoint (`/api/auth/google`).

## Hosting & Deployment

### Backend: Render
- **Host:** Render cloud hosting platform (`https://expadvisor.onrender.com/api`).
- **Server:** Gunicorn WSGI HTTP Server (`run:app`).
- **CORS:** Configured to allow cross-origin requests from frontend domains.

### Frontend: Vercel
- **Host:** Vercel static site hosting.
- **Configuration:** `vercel.json` routing rules for URL rewrite mapping HTML files and handling direct paths.

## Rate Limiting & Security

### Flask-Limiter
- **Role:** Endpoint protection against brute-force and spamming.
- **Policy:** IP-based key function (`get_remote_address`).
- **Limits:**
  - Registration: 3 requests per hour
  - Login: 5 requests per minute

*Integrations analysis: 2026-08-31*
<!-- refreshed: 2026-08-31 -->

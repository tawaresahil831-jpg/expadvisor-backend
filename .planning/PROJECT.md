# ExpAdvisor

## What This Is

ExpAdvisor is a community-driven college and career advisory platform designed for university students to share, discover, and discuss internship and placement experiences, interview journeys, academic project guidance, and course reviews. The product features an authenticated student directory, categorized experience feed, interactive problem-solving discussions with accepted solutions, and multimedia artifact attachments.

## Core Value

Empowering students with peer-sourced, authentic interview and career experience insights to make informed academic and professional decisions.

## Architecture & Technology

- **Backend:** Python Flask microservice (`backend/app/`) with SQLAlchemy ORM, JWT authentication, Flask-Limiter, and Supabase integration for object storage.
- **Frontend:** Static Multi-Page Application (MPA) in `expadvisor-frontend/frontend/` using Tailwind CSS and vanilla ES6 JavaScript via `api.js`.
- **Database & Storage:** PostgreSQL relational database with Supabase cloud storage for file attachments and avatars.

## Requirements

### Validated

- [x] Student registration and login with JWT and rate limiting
- [x] Experience posting, listing, searching, filtering, and pagination
- [x] File attachment uploads for experiences (PDF/images)
- [x] Threaded comments on experiences and accepted answers
- [x] Upvote / Like toggle on experience articles
- [x] User profile management and student directory

### Active Scope (Brownfield Roadmap)

- [ ] Clean up redundant root patch scripts and consolidate backend structure
- [ ] Migrate or bundle frontend components to avoid CDN dependencies in production
- [ ] Implement automated unit testing suite with CI pipeline (replacing script-only regression)
- [ ] Enhanced notification system and real-time community engagement

### Out of Scope

- Native mobile applications — responsive web application fulfills multi-device access.
- Complex microservice split — monolithic modular Flask app is optimal for current scale.

## Key Contacts & Repository Context

- **Worktree Root:** `/Users/sahiltaware415/Documents/ExpAdvisor`
- **Codebase Documentation:** `.planning/codebase/`
- **API Spec:** `backend/README.md`

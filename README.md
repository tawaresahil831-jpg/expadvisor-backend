# ExpAdvisor Backend

Backend API for ExpAdvisor, built with Flask and SQLAlchemy.

## Setup & Running Locally

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create a `.env` file with `DATABASE_URL`, `SECRET_KEY`, and `JWT_SECRET_KEY`.
3. Run the development server:
   ```bash
   FLASK_APP=run.py flask run --port 5001
   ```

---

## API Reference

### Base URL: `/api`

### Authentication (`/auth`)

#### 1. Register
- **URL**: `/auth/register`
- **Method**: `POST`
- **Rate Limit**: 3 per hour
- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword",
    "college": "MIT",
    "branch": "Computer Science",
    "year": 3
  }
  ```
- **Response**: `201 Created`

#### 2. Login
- **URL**: `/auth/login`
- **Method**: `POST`
- **Rate Limit**: 5 per minute
- **Request Body**:
  ```json
  {
    "email": "john@example.com",
    "password": "securepassword"
  }
  ```
- **Response**: `200 OK` (Returns JWT token in `data.token`)

#### 3. Get Current User
- **URL**: `/auth/me`
- **Method**: `GET`
- **Auth Required**: `Bearer <token>`
- **Response**: `200 OK`

---

### Experiences (`/experiences`)

#### 1. List Experiences
- **URL**: `/experiences`
- **Method**: `GET`
- **Query Params**:
  - `page` (default 1)
  - `per_page` (default 10, max 50)
  - `search` (partial match on title/content)
  - `category` (exact match)
  - `company` (exact match)
- **Response**: `200 OK` (includes `pagination` metadata)

#### 2. Get Single Experience
- **URL**: `/experiences/<id>`
- **Method**: `GET`
- **Response**: `200 OK`

#### 3. Create Experience
- **URL**: `/experiences`
- **Method**: `POST`
- **Auth Required**: `Bearer <token>`
- **Request Body**:
  ```json
  {
    "title": "Software Engineering Intern",
    "content": "Worked on backend services using Python...",
    "category": "internship",
    "semester": "6th",
    "company": "Google"
  }
  ```
- **Response**: `201 Created`

#### 4. Update Experience
- **URL**: `/experiences/<id>`
- **Method**: `PUT`
- **Auth Required**: `Bearer <token>` (Must be owner)
- **Request Body**: (Same fields as Create, all optional)
- **Response**: `200 OK`

#### 5. Delete Experience
- **URL**: `/experiences/<id>`
- **Method**: `DELETE`
- **Auth Required**: `Bearer <token>` (Must be owner)
- **Response**: `200 OK`

---

### Comments (`/experiences/<id>/comments` and `/comments/<id>`)

#### 1. Get Comments
- **URL**: `/experiences/<id>/comments`
- **Method**: `GET`
- **Response**: `200 OK`

#### 2. Add Comment
- **URL**: `/experiences/<id>/comments`
- **Method**: `POST`
- **Auth Required**: `Bearer <token>`
- **Request Body**:
  ```json
  {
    "comment": "This is very helpful, thanks!"
  }
  ```
- **Response**: `201 Created`

#### 3. Delete Comment
- **URL**: `/comments/<id>`
- **Method**: `DELETE`
- **Auth Required**: `Bearer <token>` (Must be owner)
- **Response**: `200 OK`

---

### Likes (`/experiences/<id>/like(s)`)

#### 1. Get Like Count
- **URL**: `/experiences/<id>/likes`
- **Method**: `GET`
- **Response**: `200 OK` (returns `like_count`)

#### 2. Add Like
- **URL**: `/experiences/<id>/like`
- **Method**: `POST`
- **Auth Required**: `Bearer <token>`
- **Response**: `201 Created`

#### 3. Remove Like
- **URL**: `/experiences/<id>/like`
- **Method**: `DELETE`
- **Auth Required**: `Bearer <token>` (Must be owner of like)
- **Response**: `200 OK`

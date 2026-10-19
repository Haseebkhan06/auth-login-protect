# Auth Login & Protect API

This project is part of my Week 4 backend assignment. I built a REST API using FastAPI and Supabase Authentication to handle user signup, login, logout, and protected routes.

## What I implemented

- User signup using email and password
- User login with Supabase Auth
- Access and refresh token generation
- Public route that anyone can access
- Protected profile route that requires a valid access token
- Logout endpoint
- API testing through Swagger UI

## Tech Used

- Python
- FastAPI
- Supabase
- Pydantic
- Uvicorn

## Project Structure

```text
auth-login-protect/
├── app/
│   ├── main.py
│   ├── auth.py
│   └── __init__.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd auth-login-protect
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install the required packages

```powershell
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project folder and add your Supabase project details:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
```

Replace the placeholder values with your actual Supabase URL and publishable/anon key.

### 5. Start the server

```powershell
python -m uvicorn app.main:app --port 8001
```

### 6. Open Swagger

Go to http://127.0.0.1:8001/docs to view the available endpoints and test them.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Checks if the API is running |
| GET | `/public/info` | Returns public information |
| POST | `/auth/signup` | Creates a new user |
| POST | `/auth/login` | Logs in a user and returns tokens |
| POST | `/auth/logout` | Logs out the user |
| GET | `/protected/profile` | Returns the logged-in user's profile |

## Authentication

The protected profile route requires a valid Supabase access token. Without a valid token, the request should return `401 Unauthorized`.

I used Swagger UI to test the endpoints and check how the API responds to authenticated and unauthenticated requests.

## Notes

- Email confirmation may be required during signup, depending on the Supabase settings.
- The `.env` file contains private credentials and should not be uploaded to GitHub.
- The `.gitignore` file is used to keep environment secrets and the virtual environment out of version control.

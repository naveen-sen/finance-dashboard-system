# Finance Dashboard Backend

A FastAPI-based backend API for a Finance Dashboard system. Features user/role management, transactions, dashboard analytics, JWT authentication, and SQLAlchemy/SQLModel ORM (SQLite database).

## Features
- User registration, login, role-based access control (RBAC)
- Transaction CRUD with filtering/summaries
- Dashboard metrics and charts data
- Auto DB table creation and role seeding on startup
- API documentation via Swagger/OpenAPI at `/docs`

## Prerequisites
- Python 3.10+
- Git

## Quick Start
```bash
git clone <repo>
cd "d:/Finance dashboard system"
python -m venv venv
# Activate venv (Windows: venv\Scripts\activate)
pip install -r API/requirement.txt
# Copy .env.example to .env and edit SECRET_KEY
cd API && python main.py
```
Open http://localhost:8000/docs

## Detailed Setup

### 1. Clone Repository
```bash
cd "d:/Finance dashboard system"
```

### 2. Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r API/requirement.txt
```

### 4. Environment Variables
Copy/create `API/.env`:
```
SECRET_KEY=your-super-secret-key-here  
ALGORITHM=HS256
```
**Note:** Database uses SQLite by default (`test.db` or configured in `app/db/session.py`). Tables auto-created on startup.

### 5. (Optional) Development Tools
- **Pre-commit:**
  ```bash
  pip install pre-commit
  pre-commit install
  ```
  Runs on git commit (black, isort, mypy, etc.). See `pre-commit_readme.md` for details.
- **Mypy:** Static type checking.
  ```bash
  cd API && mypy .
  ```

### 6. Run the Server
```bash
cd API
python main.py
```
- Server starts at http://0.0.0.0:8000
- Access Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

On first run: Roles are auto-seeded (admin, user, etc.).

## Project Structure
```
API/
├── main.py                 # FastAPI app entry
├── requirement.txt         # Dependencies
├── app/
│   ├── config.py           # Settings (.env)
│   ├── db/                 # SQLAlchemy session, base
│   ├── Models/             # SQLModel (User, Role, Transaction, etc.)
│   ├── Schema/             # Pydantic schemas
│   ├── Routes/             # API routers (users, roles, transactions, dashboard)
│   ├── Services/           # Business logic
│   ├── auth/               # JWT, access control
│   └── utils/
└── test.db                 # SQLite DB (auto-created)
```

## API Usage Example
- POST /auth/register (create user)
- POST /auth/login (JWT token)
- GET /api/users (with Authorization: Bearer <token>)

## Troubleshooting
- **DB not creating:** Check `app/db/session.py` for engine URL (default sqlite:///./test.db).
- **Port in use:** Change port in `main.py`.
- **Pre-commit issues:** `pre-commit run --all-files`.
- **Dependencies errors:** Ensure venv active, pip install --upgrade pip.

## Deployment
- Use gunicorn + uvicorn for prod: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`
- Dockerize or deploy to Railway/Vercel/Render.


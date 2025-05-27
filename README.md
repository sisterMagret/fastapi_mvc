
# FastAPI MVC Application

A web application following MVC pattern with FastAPI, SQLAlchemy, and JWT authentication.

## Project Structure

```
fastapi_mvc_app/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app initialization
│   ├── config.py                # Application configuration
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py              # Base database setup
│   │   ├── models               # SQLAlchemy models
│   │   |   ├── posts.py
│   │   |   ├── users.py
│   │   └── session.py           # Database session management
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py              # Authentication dependencies
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Auth routes (login, signup)
│   │   └── posts.py             # Post-related routes
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py              # Auth Pydantic models
│   │   ├── posts.py             # Post Pydantic models
│   │   └── responses.py         # Common response models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py              # Auth business logic
│   │   ├── cache.py             # Caching service
│   │   └── posts.py             # Posts business logic
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py        # Custom exceptions
│       └── security.py          # Security utilities
├── tests/                       # Test directory
├── requirements.txt             # Project dependencies
├── README.md                    # This file
└── .env                         # Environment variables
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- MySQL server
- pip (Python package manager)

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/fastapi_mvc_app.git
cd fastapi_mvc
```

### 3. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Database Setup

1. Create a MySQL database:
```sql
CREATE DATABASE fastapi_mvc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Create a MySQL user with privileges:
```sql
CREATE USER 'fastapi_user'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON fastapi_mvc.* TO 'fastapi_user'@'localhost';
FLUSH PRIVILEGES;
```

### 6. Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=mysql+pymysql://fastapi_user:yourpassword@localhost:3306/fastapi_mvc
JWT_SECRET_KEY=your-secret-key-here
```

### 7. Run the Application

```bash
uvicorn app.main:app --reload
```

The application will be available at:
- http://localhost:8000
- Interactive docs: http://localhost:8000/
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login

### Posts
- `POST /posts/` - Create a post (requires auth)
- `GET /posts/` - Get all user's posts (requires auth)
- `DELETE /posts/{post_id}` - Delete a post (requires auth)

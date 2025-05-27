from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base
from app.database.session import engine
from app.routes import auth, posts


def create_tables():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


def get_application():
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="FastAPI MVC App",
        description="A web application following MVC pattern with FastAPI.",
        version="1.0.0",
        docs_url="/"
    )

    # Setup CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth.router)
    app.include_router(posts.router)

    # Create tables on startup
    @app.on_event("startup")
    async def startup():
        create_tables()

    return app


app = get_application()
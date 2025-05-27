from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import UserCreate, Token
from app.services.auth import AuthService
from app.utils.exceptions import AuthenticationError, UserAlreadyExistsError
from app.config import settings


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Endpoint for user registration."""
    try:
        user = AuthService.create_user(db, user_data)
        access_token = AuthService.create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer", "user": user}
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Endpoint for user login.
    
    Args:
        form_data: Login form data (username=email, password).
        db: Database session.
        
    Returns:
        Token: JWT access token.
        
    Raises:
        HTTPException: If authentication fails.
    """
    try:
        user = AuthService.authenticate_user(
            db,
            email=form_data.username,
            password=form_data.password
        )
        access_token = AuthService.create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer", "user": user}
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models import User
from app.schemas.auth import UserCreate
from app.utils.exceptions import (
    AuthenticationError,
    UserAlreadyExistsError,
)

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


class AuthService:
    """Service handling authentication-related operations."""

    @staticmethod
    def verify_password(
        plain_password: str, hashed_password: str
    ) -> bool:
        """Verify a password against its hash.

        Args:
            plain_password: The plain text password to verify.
            hashed_password: The hashed password to compare against.

        Returns:
            bool: True if passwords match, False otherwise.
        """
        return pwd_context.verify(
            plain_password, hashed_password
        )

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate a password hash.

        Args:
            password: The plain text password to hash.

        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """Create a JWT access token.

        Args:
            data: The data to encode in the token.
            expires_delta: Optional expiration time delta.

        Returns:
            str: The encoded JWT token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=15
            )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    @classmethod
    def authenticate_user(
        cls, db: Session, email: str, password: str
    ) -> User:
        """Authenticate a user.

        Args:
            db: Database session.
            email: User's email.
            password: User's password.

        Returns:
            User: The authenticated user.

        Raises:
            AuthenticationError: If authentication fails.
        """
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )
        if not user or not cls.verify_password(
            password, user.password_hash
        ):
            raise AuthenticationError(
                "Incorrect email or password"
            )
        return user

    @classmethod
    def create_user(
        cls, db: Session, user_data: UserCreate
    ) -> User:
        """Create a new user.

        Args:
            db: Database session.
            user_data: User creation data.

        Returns:
            User: The created user.

        Raises:
            UserAlreadyExistsError: If user with email already exists.
        """
        existing_user = (
            db.query(User)
            .filter(User.email == user_data.email)
            .first()
        )
        if existing_user:
            raise UserAlreadyExistsError(
                "User with this email already exists"
            )

        hashed_password = cls.get_password_hash(
            user_data.password
        )
        user = User(
            email=user_data.email,
            password_hash=hashed_password,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

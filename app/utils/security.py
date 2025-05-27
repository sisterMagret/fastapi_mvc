import re
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from typing import Optional

from app.config import settings
from app.utils.exceptions import SecurityException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityUtils:
    """Utility class for security-related operations."""
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """Validate password meets strength requirements.
        
        Args:
            password: The password to validate
            
        Returns:
            bool: True if password meets requirements
            
        Raises:
            SecurityException: If password doesn't meet requirements
        """
        if len(password) < 8:
            raise SecurityException("Password must be at least 8 characters long")
        if not re.search("[a-z]", password):
            raise SecurityException("Password must contain at least one lowercase letter")
        if not re.search("[A-Z]", password):
            raise SecurityException("Password must contain at least one uppercase letter")
        if not re.search("[0-9]", password):
            raise SecurityException("Password must contain at least one digit")
        if not re.search("[^a-zA-Z0-9]", password):
            raise SecurityException("Password must contain at least one special character")
        return True

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate a secure password hash.
        
        Args:
            password: The plain text password
            
        Returns:
            str: The hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash.
        
        Args:
            plain_password: The plain text password
            hashed_password: The hashed password
            
        Returns:
            bool: True if passwords match
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token.
        
        Args:
            data: The data to encode in the token
            expires_delta: Optional expiration time delta
            
        Returns:
            str: The encoded JWT token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode a JWT token.
        
        Args:
            token: The JWT token to decode
            
        Returns:
            dict: The decoded token payload
            
        Raises:
            SecurityException: If token is invalid
        """
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise SecurityException("Token has expired")
        except jwt.JWTError:
            raise SecurityException("Invalid token")
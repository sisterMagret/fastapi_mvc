import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from datetime import timedelta

from app.services.auth import AuthService
from app.services.posts import PostService
from app.services.cache import CacheService
from app.database.models import User, Post
from app.utils.exceptions import AuthenticationError, UserAlreadyExistsError

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

class TestAuthService:
    """Unit tests for AuthService."""
    
    def test_verify_password(self):
        password = "SecurePass123!"
        hashed = AuthService.get_password_hash(password)
        assert AuthService.verify_password(password, hashed) is True
        assert AuthService.verify_password("wrongpass", hashed) is False

    def test_create_access_token(self):
        token = AuthService.create_access_token({"sub": "123"})
        assert isinstance(token, str)
        assert len(token) > 0

    def test_authenticate_user_success(self, mock_db):
        mock_user = User(email="test@example.com", password_hash=AuthService.get_password_hash("password"))
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        user = AuthService.authenticate_user(mock_db, "test@example.com", "password")
        assert user == mock_user

    def test_authenticate_user_failure(self, mock_db):
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with pytest.raises(AuthenticationError):
            AuthService.authenticate_user(mock_db, "test@example.com", "password")

    def test_create_user_success(self, mock_db):
        mock_db.query.return_value.filter.return_value.first.return_value = None
        user_data = {"email": "new@example.com", "password": "SecurePass123!"}
        
        user = AuthService.create_user(mock_db, user_data)
        assert mock_db.add.called
        assert mock_db.commit.called
        assert isinstance(user, User)

    def test_create_user_exists(self, mock_db):
        mock_db.query.return_value.filter.return_value.first.return_value = User()
        user_data = {"email": "exists@example.com", "password": "SecurePass123!"}
        
        with pytest.raises(UserAlreadyExistsError):
            AuthService.create_user(mock_db, user_data)

class TestPostService:
    """Unit tests for PostService."""
    
    def test_create_post(self, mock_db):
        post = PostService.create_post(mock_db, "Test post", 1)
        assert mock_db.add.called
        assert mock_db.commit.called
        assert isinstance(post, Post)

    def test_get_user_posts(self, mock_db):
        mock_posts = [Post(text="Post 1"), Post(text="Post 2")]
        mock_db.query.return_value.filter.return_value.all.return_value = mock_posts
        
        posts = PostService.get_user_posts(mock_db, 1)
        assert len(posts) == 2
        assert all(isinstance(p, Post) for p in posts)

class TestCacheService:
    """Unit tests for CacheService."""
    
    def test_cache_operations(self):
        CacheService.set("test_key", {"data": 123})
        assert CacheService.get("test_key") == {"data": 123}
        
        # Test expiration
        CacheService.set("temp_key", {"data": 456}, expire_seconds=-1)
        assert CacheService.get("temp_key") is None
from datetime import datetime, timedelta
from typing import Any, Dict, Optional


from app.config import settings


class CacheService:
    """Service handling in-memory caching."""
    
    _cache: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def get(cls, key: str) -> Optional[Dict[str, Any]]:
        """Get cached data.
        
        Args:
            key: Cache key.
            
        Returns:
            Optional[Dict]: Cached data if exists and not expired, else None.
        """
        cached_data = cls._cache.get(key)
        if cached_data and datetime.now() < cached_data["expires_at"]:
            return cached_data["data"]
        cls._cache.pop(key, None)
        return None

    @classmethod
    def set(cls, key: str, data: Any, expire_seconds: int = None) -> None:
        """Set data in cache.
        
        Args:
            key: Cache key.
            data: Data to cache.
            expire_seconds: Cache expiration in seconds.
        """
        expire_seconds = expire_seconds or settings.CACHE_EXPIRE_SECONDS
        cls._cache[key] = {
            "data": data,
            "expires_at": datetime.now() + timedelta(seconds=expire_seconds)
        }
        
    @classmethod
    def delete(cls, key: str, post_id: str) -> None:
        """Delete cached data.
        
        Args:
            key: Cache key.
            
        Returns:
            None.
        """
        cached_data = cls._cache.get(key)
        if cached_data:
            cached_data.pop(post_id, None)
        return None
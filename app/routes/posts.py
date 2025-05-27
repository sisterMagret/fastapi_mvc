from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.database.models.users import User
from app.database.session import get_db
from app.dependencies.auth import get_current_user, validate_post_size
from app.schemas import PostCreate, PostResponse
from app.services import PostService
from app.services import CacheService
from app.utils.exceptions import PostNotFoundError, UnauthorizedError


router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    request: Request,
    post_data: PostCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _: None = Depends(validate_post_size)
):
    """Endpoint to create a new post.
    
    Args:
        request: FastAPI request object.
        post_data: Post creation data.
        user: Authenticated user.
        db: Database session.
        
    Returns:
        PostResponse: Created post data.
    """
    post = PostService.create_post(db, text=post_data.text, owner_id=user.id)
    return post


@router.get("/", response_model=List[PostResponse])
def get_posts(
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Endpoint to get all posts for the current user.
    
    Args:
        request: FastAPI request object.
        user: Authenticated user.
        db: Database session.
        
    Returns:
        List[PostResponse]: List of user's posts.
    """
    cache_key = f"user_posts_{user.id}"
    cached_data = CacheService.get(cache_key)
    if cached_data:
        return cached_data
        
    posts = PostService.get_user_posts(db, user_id=user.id)
    CacheService.set(cache_key, posts)
    return posts


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Endpoint to delete a post.
    
    Args:
        post_id: ID of the post to delete.
        user: Authenticated user.
        db: Database session.
        
    Raises:
        HTTPException: If post not found or unauthorized.
    """
    try:
        PostService.delete_post(db, post_id=post_id, user_id=user.id)
        cache_key = f"user_posts_{user.id}"
        _ = CacheService.delete(cache_key, post_id)
      
    except (PostNotFoundError, UnauthorizedError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if isinstance(e, PostNotFoundError) 
                else status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
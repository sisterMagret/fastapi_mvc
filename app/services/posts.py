from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.config import settings
from app.database.models import Post
from app.schemas.posts import PostCreate, PostResponse
from app.utils.exceptions import PostNotFoundError, UnauthorizedError


class PostService:
    """Service handling post-related operations."""
    
    @staticmethod
    def create_post(db: Session, text: str, owner_id: int) -> Post:
        """Create a new post.
        
        Args:
            db: Database session.
            text: Content of the post.
            owner_id: ID of the post owner.
            
        Returns:
            Post: The created post.
        """
        post = Post(text=text, owner_id=owner_id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def get_user_posts(db: Session, user_id: int) -> List[Post]:
        """Get all posts for a user.
        
        Args:
            db: Database session.
            user_id: ID of the user.
            
        Returns:
            List[Post]: List of user's posts.
        """
        return db.query(Post).filter(Post.owner_id == user_id).all()

    @staticmethod
    def delete_post(db: Session, post_id: int, user_id: int) -> None:
        """Delete a post.
        
        Args:
            db: Database session.
            post_id: ID of the post to delete.
            user_id: ID of the user attempting deletion.
            
        Raises:
            PostNotFoundError: If post doesn't exist.
            UnauthorizedError: If user doesn't own the post.
        """
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise PostNotFoundError("Post not found")
        if post.owner_id != user_id:
            raise UnauthorizedError("You don't have permission to delete this post")
            
        db.delete(post)
        db.commit()
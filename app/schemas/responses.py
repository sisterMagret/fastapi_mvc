from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response schema."""
    success: bool = Field(True, description="Indicates if the request was successful")
    data: T = Field(..., description="The response data")
    message: Optional[str] = Field(None, description="Optional success message")

class ErrorResponse(BaseModel):
    """Standard error response schema."""
    success: bool = Field(False, description="Indicates if the request failed")
    error: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")

class TokenResponse(SuccessResponse):
    """Token response schema extending success response."""
    data: str = Field(..., description="JWT token")

class PostListResponse(SuccessResponse):
    """Post list response schema."""
    class PostData(BaseModel):
        id: int
        text: str
        owner_id: int
    
    data: list[PostData] = Field(..., description="List of posts")
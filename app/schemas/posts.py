from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    """Schema for creating a new post."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Content of the post (1-10000 characters).",
    )


class PostResponse(BaseModel):
    """Schema for post response."""

    id: int = Field(
        ..., description="Unique identifier of the post."
    )
    text: str = Field(
        ..., description="Content of the post."
    )
    owner_id: int = Field(
        ..., description="ID of the post owner."
    )


class PostDelete(BaseModel):
    """Schema for deleting a post."""

    post_id: int = Field(
        ..., description="ID of the post to delete."
    )

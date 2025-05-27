from pydantic import BaseModel, EmailStr, Field


class UserRead(BaseModel):
    email: EmailStr = Field(
        ..., description="User's email address."
    )
    id: int = Field(..., description="User's ID.")


class UserCreate(BaseModel):
    """Schema for user creation (signup)."""

    email: EmailStr = Field(
        ..., description="User's email address."
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        description="User's password (8-64 characters).",
    )


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr = Field(
        ..., description="User's email address."
    )
    password: str = Field(
        ..., description="User's password."
    )


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str = Field(
        ..., description="JWT access token."
    )
    token_type: str = Field(
        "bearer", description="Token type."
    )
    user: UserRead

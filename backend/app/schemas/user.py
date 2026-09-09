from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class RoleRead(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    id: int
    email: str = Field(..., max_length=255)
    full_name: str
    is_active: bool
    is_superuser: bool
    preferred_currency: str
    timezone: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=2, max_length=100)
    preferred_currency: str | None = Field(None, max_length=10)
    timezone: str | None = Field(None, max_length=50)


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)

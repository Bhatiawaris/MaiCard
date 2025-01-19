import uuid
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, Dict, List
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from sqlalchemy import Column
from pgvector.sqlalchemy import Vector

# Shared properties for User
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = Field(default=None, max_length=255)

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

# Properties to receive via API on update
class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(default=None, max_length=255)  # type: ignore
    password: Optional[str] = Field(default=None, min_length=8, max_length=40)

# Database model for User
class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str
    contacts: Optional[Dict] = Field(default=None, sa_column=Column(JSONB))
    profiles: List["Profile"] = Relationship(back_populates="user")  # Relationship to Profile

# Database model for Profile
class Profile(SQLModel, table=True):
    profile_id: Optional[int] = Field(default=None, primary_key=True)  # Matches SERIAL
    user_id: int = Field(foreign_key="user.user_id")  # Foreign key constraint
    type: str = Field(sa_column=Column(ENUM("networking", "friends", "dating", name="profile_type")))  # Enum type
    contacts: Optional[Dict] = Field(default=None, sa_column=Column(JSONB))  # Matches JSONB
    text: Optional[str] = Field(default=None)  # Matches TEXT
    vector_embeddings: Optional[List[float]] = Field(
        sa_column=Column(Vector(1024), nullable=True)  # Explicit mapping to PostgreSQL vector type
    )
    user: "User" = Relationship(back_populates="profiles")  # Relationship to User

# Properties to return via API for Profile
class ProfilePublic(SQLModel):
    profile_id: int
    user_id: int
    type: str
    contacts: Optional[Dict]
    text: Optional[str]
    vector_embeddings: Optional[List[float]]

class ProfileCreate(SQLModel):
    user_id: int
    username: str
    type: str
    contacts: Optional[Dict] = None
    text: Optional[str] = None
    color: Optional[str] = None
    vector_embeddings: Optional[List[float]] = None

class ProfileUpdate(SQLModel):
    profile_id: int
    type: Optional[str] = None  # Allow updating the type
    contacts: Optional[Dict] = None  # Allow updating contacts
    text: Optional[str] = None  # Allow updating text
    vector_embeddings: Optional[List[float]] = None  
   
# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int  # Use `user_id` as `id` for public responses

class UsersPublic(SQLModel):
    data: List[UserPublic]
    count: int

# Generic message
class Message(SQLModel):
    message: str

# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# Contents of JWT token
class TokenPayload(SQLModel):
    sub: Optional[str] = None

class SaveProfile(SQLModel):
    profile_id1: int
    profile_id2 : int
    username: str
    contacts: Optional[Dict] = None
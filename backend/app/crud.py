import uuid
from typing import Any, Dict
from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate, Profile
from pgvector.sqlalchemy import Vector


def create_user(*, session: Session, user_create: UserCreate, contacts: Dict = None) -> User:
    """
    Create a new user in the database.
    """
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_password,
        contacts=contacts,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    """
    Update an existing user in the database.
    """
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """
    Retrieve a user by email from the database.
    """
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    """
    Authenticate a user by verifying their email and password.
    """
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

def create_profile(
    *, 
    session: Session, 
    user_id: int, 
    profile_type: str, 
    contacts: Dict = None, 
    text: str = None, 
    vector_embeddings: list[float] = None
) -> Profile:
    
    user = session.get(User, user_id)
    if not user:
        raise ValueError(f"User with id {user_id} does not exist.")

    # Ensure `vector_embeddings` is a list of floats
    if vector_embeddings and not isinstance(vector_embeddings, list):
        raise ValueError("vector_embeddings must be a list of floats.")

    db_profile = Profile(
        user_id=user_id,
        type=profile_type,
        contacts=contacts,
        text=text,
        vector_embeddings=vector_embeddings,  # This will map to the `vector(1024)` type
    )
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)
    return db_profile
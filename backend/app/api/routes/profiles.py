from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import SessionDep, get_current_active_user
from app.models import Profile, ProfilePublic, ProfileCreate, ProfileUpdate, User

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("/", response_model=ProfilePublic)
def create_profile(
    session: SessionDep, profile_in: ProfileCreate, current_user: User = Depends(get_current_active_user)
) -> ProfilePublic:
    """
    Create a new profile for the current user.
    """
    profile = Profile(
        user_id=current_user.user_id,
        type=profile_in.type,
        contacts=profile_in.contacts,
        text=profile_in.text,
        vector_embeddings=profile_in.vector_embeddings,
    )
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.get("/", response_model=list[ProfilePublic])
def read_profiles(
    session: SessionDep, current_user: User = Depends(get_current_active_user)
) -> list[ProfilePublic]:
    """
    Retrieve all profiles for the current user.
    """
    profiles = session.exec(select(Profile).where(Profile.user_id == current_user.user_id)).all()
    return profiles

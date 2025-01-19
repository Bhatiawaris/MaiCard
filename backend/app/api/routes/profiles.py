from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import SessionDep, get_current_active_user
from app.models import Profile, ProfilePublic, ProfileCreate, ProfileUpdate, User
from app.core.DBHelper import DBHelper

router = APIRouter(prefix="/profiles", tags=["profiles"])
db = DBHelper()

# @router.post("/", response_model=ProfilePublic)
# def create_profile(
#     session: SessionDep, profile_in: ProfileCreate, current_user: User = Depends(get_current_active_user)
# ) -> ProfilePublic:
#     """
#     Create a new profile for the current user.
#     """
#     profile = Profile(
#         user_id=current_user.user_id,
#         type=profile_in.type,
#         contacts=profile_in.contacts,
#         text=profile_in.text,
#         vector_embeddings=profile_in.vector_embeddings,
#     )
#     session.add(profile)
#     session.commit()
#     session.refresh(profile)
#     return profile


# @router.get("/", response_model=list[ProfilePublic])
# def read_profiles(
#     session: SessionDep, current_user: User = Depends(get_current_active_user)
# ) -> list[ProfilePublic]:
#     """
#     Retrieve all profiles for the current user.
#     """
#     profiles = session.exec(select(Profile).where(Profile.user_id == current_user.user_id)).all()
#     return profiles


# Define the GET route for fetching user profile by ID
@router.get("/{profile_id}")
def get_user(profile_id: int):
    # Fetch profile from the database
    profile = db.getProfile(profile_id)
    
    # Handle case where profile is not found
    if profile is None or profile == []:
        return HTTPException(status_code=404, detail="Profile not found")
    
    return profile

@router.post("/createProfile")
async def create_profile(profile: ProfileCreate):
    # Extract data from the request body
    db = DBHelper()
    print(profile)
    try:
        result = db.createProfile(profile.user_id, profile.type, profile.contacts, profile.text)
        if result:
            return {"message" : "success"}
        else:
            raise HTTPException(status_code=404)
    except Exception as e:
        print(e)
        return HTTPException(status_code=404, detail = e)
    
@router.delete("/deleteProfile/{profile_id}")
async def create_profile(profile_id: int):
    # Extract data from the request body
    try:
        result = db.deleteProfile(profile_id)
        if result:
            return {"message" : "success"}
        else:
            return HTTPException(status_code=404)
    except Exception as e:
        return HTTPException(status_code=404, detail = e)
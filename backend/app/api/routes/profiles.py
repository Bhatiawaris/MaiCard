from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import SessionDep, get_current_active_user
from app.models import Profile, ProfilePublic, ProfileCreate, ProfileUpdate, User, SaveProfile
from app.core.DBHelper import DBHelper

router = APIRouter(prefix="/profiles", tags=["profiles"])
db = DBHelper()

# Define the GET route for fetching user profile by ID
@router.get("/{profile_id}")
def get_profile(profile_id: int):
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
            return HTTPException(status_code=404)
    except Exception as e:
        print(e)
        return HTTPException(status_code=404, detail = e)
    
@router.delete("/deleteProfile/{profile_id}")
async def delete_profile(profile_id: int):
    # Extract data from the request body
    try:
        result = db.deleteProfile(profile_id)
        if result:
            return {"message" : "success"}
        else:
            return HTTPException(status_code=404)
    except Exception as e:
        return HTTPException(status_code=404, detail = e)

@router.post("/updateProfile")
async def update_profile(profile: ProfileUpdate):
    # Extract data from the request body
    db = DBHelper()
    print(profile)
    try:
        result = db.updateProfile(profile.user_id, profile.type, profile.contacts, profile.text)
        if result:
            return {"message" : "success"}
        else:
            return HTTPException(status_code=404)
    except Exception as e:
        print(e)
        return HTTPException(status_code=404, detail = e)
    

@router.post("/saveProfile")
async def save_profile(save: SaveProfile):
    # Extract data from the request body
    db = DBHelper()
    try:
        result = db.saveProfile(save.user_id, save.profile_id)
        if result:
            return {"message" : "success"}
        else:
            return HTTPException(status_code=404)
    except Exception as e:
        print(e)
        return HTTPException(status_code=404, detail = e)

@router.get("/getSaves/{user_id}")
async def get_saves(user_id: int):
    # Extract data from the request body
    db = DBHelper()
    try:
        result = db.getSaves(user_id)
        if result:
            return result
        else:
            return HTTPException(status_code=404)
    except Exception as e:
        print(e)
        return HTTPException(status_code=404, detail = e)
    
@router.get("/getProfiles/{user_id}")
async def get_saves(user_id: int):
    # Extract data from the request body
    db = DBHelper()
    try:
        result = db.getProfiles(user_id)
        return result
    except Exception as e:
        print(e)
        return HTTPException(status_code=404, detail = e)
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import SessionDep, get_current_active_user
from app.models import Profile, ProfilePublic, ProfileCreate, ProfileUpdate, User, SaveProfile
from app.core.DBHelper import DBHelper
from app.bgem3 import BGEM3Service
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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
        profile_id = db.createProfile(profile.user_id, profile.username, profile.type, profile.contacts, profile.text, profile.color)

        if not profile_id:
            return HTTPException(status_code=404)
        
        try:
            # Embed the text using BGEM3Service
            embeddings = db.createEmbeddings(profile.text, profile_id)
            
            if embeddings is None:
                raise HTTPException(status_code=500, detail="Failed to generate embeddings")

            # Update the profile with the generated embeddings
            db.supabase.table("profiles").update({
                "vector_embeddings": embeddings
            }).eq("user_id", profile.user_id).execute()
        
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise HTTPException(status_code=500, detail=f"Error generating embeddings: {e}")
        
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
    print(save)
    db = DBHelper()
    try:
        # Retrieve and parse embeddings
        my_embeddings = db.getEmbeddings(save.profile_id1)  # e.g., '[-1.0099975e-05,0.04453614,...]'
        other_embeddings = db.getEmbeddings(save.profile_id2) 

        # Ensure embeddings are not None
        if not my_embeddings or not other_embeddings:
            raise HTTPException(status_code=404, detail="Embeddings not found for one or both profiles")

        # Parse the string embeddings into numeric arrays
        my_embeddings = np.array(eval(my_embeddings))  # Convert string to array
        other_embeddings = np.array(eval(other_embeddings))

        # Calculate cosine similarity
        cosine_similarity_result = cosine_similarity(my_embeddings.reshape(1, -1), other_embeddings.reshape(1, -1))

        # Extract the similarity score

        cos = int(cosine_similarity_result[0][0] * 100)

        result = db.saveProfile(save.profile_id1, save.profile_id2, cos)
        
        if result:
            return {"message" : "success"}
        else:
            return HTTPException(status_code=404)
    except Exception as e:
        print(e)
        return HTTPException(status_code=404, detail = e)

@router.get("/getSaves/{profile_id}")
async def get_saves(profile_id: int):
    # Extract data from the request body
    db = DBHelper()
    try:
        result = db.getSaves(profile_id)
        if result:
            return result
        else:
            return HTTPException(status_code=404)
    except Exception as e:
        print(e)
        return HTTPException(status_code=404, detail = e)
    
@router.get("/getProfiles/{user_id}")
async def get_profiles(user_id: int):
    # Extract data from the request body
    db = DBHelper()
    try:
        result = db.getProfiles(user_id)
        return result
    except Exception as e:
        print(e)
        return HTTPException(status_code=404, detail = e)
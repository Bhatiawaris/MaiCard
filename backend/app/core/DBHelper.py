import os
from supabase import create_client, Client
from datetime import datetime
from app.bgem3 import BGEM3Service
from app.core.config import settings

URL = settings.SUPABASE_URL
KEY = settings.SUPABASE_KEY

class DBHelper():
    def __init__(self):
        try:
            self.supabase = create_client(URL, KEY)

        except Exception as e:
            print(f"An error occurred: {e}")

    # get contacts of a profile, this is used when someone scans someone else
    def getProfile(self, profile_id):
        query = self.supabase.table("profiles").select("*").eq('profile_id', profile_id).execute()
        return query.data[0]
    
    # get a users profiles
    def getProfiles(self, user_id):
        query = self.supabase.table("profiles").select("*").eq('user_id', user_id).execute()
        return query.data

    # gets a users saves
    def getSaves(self, my_profile_id):
        query = self.supabase.table("saves").select("*").eq("my_profile_id", my_profile_id).execute()
        result = []
        for entry in query.data:
            profile = self.getProfile(entry["other_profile_id"])
            result.append({
                "username" : profile["username"],
                "contacts" : profile["contacts"],
                "date_saved" : entry["date_saved"],
                "compatability_score": entry["compatability_score"]
            })
        return result

    
    # saves a profile to a user's account
    def saveProfile(self, profile_id1, profile_id2, compatability_score):
        entry = {
            "my_profile_id" : profile_id1,
            "other_profile_id" : profile_id2,
            "date_saved" : datetime.now().strftime("%Y-%m-%d"),
            "compatability_score": compatability_score
        }
        try: 
            self.supabase.table("saves").insert(entry).execute()
            return True
        except Exception as e:
            print(f"Error has occured: {e}")
            return False

    # creates a profile, profile_type is limited to following options:
    # "networking" | "dating" | "freinds"
    def createProfile(self, user_id, username, profile_type, contacts, text, color):
        query = self.supabase.table("profiles").select("profile_id").order('profile_id', desc=True).limit(1).execute()
        latest_id = query.data[0]
        profile_id = int(latest_id["profile_id"]) + 1
        entry = {
            "profile_id" : profile_id,
            "user_id" : user_id,
            "username" : username,
            "type" : profile_type,
            "contacts" : contacts,
            "text" : text,
            "color" : color
        }
        try: 
            self.supabase.table("profiles").insert(entry).execute()
            return profile_id
        except Exception as e:
            print(f"Error has occured: {e}")
            return False

    # updates a profile, profile_type is limited to following options:
    # "networking" | "dating" | "freinds"
    def updateProfile(self, profile_id, profile_type, contacts, text):
        entry = {
            "type" : profile_type,
            "contacts" : contacts,
            "text" : text
        }
        try: 
            self.supabase.table("profiles").update(entry).eq("profile_id", profile_id).execute()
            return True
        except Exception as e:
            print(f"Error has occured: {e}")
            return False
    
    # deletes a profile
    def deleteProfile(self, profile_id):
        try: 
            self.supabase.table("profiles").delete().eq("profile_id", profile_id).execute()
            return True
        except Exception as e:
            print(f"Error has occured: {e}")
            return False
    
    # registers a user
    def registerUser(self, email, hashed_password, contacts):
        query = self.supabase.table("users").select("user_id").order('user_id', desc=True).limit(1).execute()
        latest_id = query.data[0]
        user_id = int(latest_id["user_id"]) + 1
        entry = {
            "user_id" : user_id,
            "email" : email,
            "hashed_password" : hashed_password,
            "contacts" : contacts

        }
        try: 
            self.supabase.table("users").insert(entry).execute()
            return True
        except Exception as e:
            print(f"Error has occured: {e}")
            return False
    
    # logs in a user
    def loginUser(self, email, hashed_password):
        try: 
            query = self.supabase.table("users").select("user_id").eq("email", email).eq("hashed_password", hashed_password).execute()
            return query.data[0]
        except Exception as e:
            print(f"Error has occured: {e}")
            return None

    # Generate and update vector embeddings for profiles
    def createEmbeddings(self, text: str, profile_id: int):
        bgem3_service = BGEM3Service()
        try:
            # Generate vector embeddings using BGEM3
            embeddings = bgem3_service.embed_text(text)

            if embeddings is None or not isinstance(embeddings, list):
                print(f"Failed to generate embeddings for user {profile_id}.")
                return False

            # Update the vector_embeddings column for the specified profile
            self.supabase.table("profiles").update({
                "vector_embeddings": embeddings
            }).eq("profile_id", profile_id).execute()

            print(f"Vector embeddings updated successfully for profile_id {profile_id}.")
            return True
        except Exception as e:
            print(f"Error while creating embeddings for profile_id {profile_id}: {e}")
            return False

    def getEmbeddings(self, profile_id):
        try:
            # Query the profiles table for the vector_embeddings of the given profile_id
            query = self.supabase.table("profiles").select("vector_embeddings").eq("profile_id", profile_id).execute()
            
            # Check if data exists
            if not query.data:
                print(f"No embeddings found for profile_id {profile_id}.")
                return None
            
            # Return the embeddings
            return query.data[0].get("vector_embeddings")
        except Exception as e:
            print(f"Error retrieving embeddings for profile_id {profile_id}: {e}")
            return None
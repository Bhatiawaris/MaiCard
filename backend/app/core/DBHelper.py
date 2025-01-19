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
            self.bgem3_service = BGEM3Service()

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
    def getSaves(self, user_id):
        query = self.supabase.table("saves").select("profile_id, date_saved").eq("user_id", user_id).execute()
        result = []
        for entry in query.data:
            profile = self.getProfile(entry["profile_id"])
            result.append({
                "profile" : profile,
                "date_saved" : entry["date_saved"]
            })
        return result
    
    # saves a profile to a user's account
    def saveProfile(self, user_id, profile_id):
        entry = {
            "user_id" : user_id,
            "profile_id" : profile_id,
            "date_saved" : datetime.now().strftime("%Y-%m-%d")
        }
        try: 
            self.supabase.table("saves").insert(entry).execute()
            return True
        except Exception as e:
            print(f"Error has occured: {e}")
            return False

    # creates a profile, profile_type is limited to following options:
    # "networking" | "dating" | "freinds"
    def createProfile(self, user_id, profile_type, contacts, text):
        query = self.supabase.table("profiles").select("profile_id").order('profile_id', desc=True).limit(1).execute()
        latest_id = query.data[0]
        profile_id = int(latest_id["profile_id"]) + 1
        entry = {
            "profile_id" : profile_id,
            "user_id" : user_id,
            "type" : profile_type,
            "contacts" : contacts,
            "text" : text
        }
        try: 
            self.supabase.table("profiles").insert(entry).execute()
            return True
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
    def registerUser(self, email, hashed_password):
        query = self.supabase.table("users").select("user_id").order('user_id', desc=True).limit(1).execute()
        latest_id = query.data[0]
        user_id = int(latest_id["user_id"]) + 1
        entry = {
            "user_id" : user_id,
            "email" : email,
            "hashed_password" : hashed_password
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
    def createEmbeddings(self):
        try:
            # Fetch all profiles with non-null text
            query = self.supabase.table("profiles").select("profile_id, text").not_("text", "is.null").execute()
            profiles = query.data
            
            if not profiles:
                print("No profiles with non-null text found.")
                return False

            for profile in profiles:
                profile_id = profile["profile_id"]
                text = profile["text"]

                # Generate vector embeddings using BGEM3
                embeddings = self.bgem3_service.embed_text(text)

                if embeddings is None:
                    print(f"Failed to generate embeddings for profile_id {profile_id}. Skipping.")
                    continue

                # Update the vector_embeddings column
                update_response = self.supabase.table("profiles").update({
                    "vector_embeddings": embeddings
                }).eq("profile_id", profile_id).execute()

                if update_response.status_code not in (200, 204):  # Ensure update was successful
                    print(f"Failed to update profile_id {profile_id}: {update_response.data}")
                    continue

            print("Vector embeddings updated successfully.")
            return True
        except Exception as e:
            print(f"Error while creating embeddings: {e}")
            return False

import os
from supabase import create_client, Client
from datetime import datetime

URL = "https://fdsxeayozansnwmmcvrb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZkc3hlYXlvemFuc253bW1jdnJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzcyMzIwNzAsImV4cCI6MjA1MjgwODA3MH0.1TmaRj3YDRQ94Z1EepsMNnv1JwCWmn49vj7AyDc8FAk"

class DBHelper():
    def __init__(self):
        try:
            self.supabase = create_client(URL, KEY)

        except Exception as e:
            print(f"An error occurred: {e}")

    # get contacts of a profile, this is used when someone scans someone else
    def getProfile(self, profile_id):
        print("AM I FUCKING WORKING?")
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
    def saveProfile(self, profile_id1, profile_id2, contacts, username):
        entry = {
            "my_profile_id" : profile_id1,
            "other_profile_id" : profile_id2,
            "date_saved" : datetime.now().strftime("%Y-%m-%d"),
            "contacts" : contacts,
            "username" : username
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
            query = self.supabase.table("users").select("*").eq("email", email).eq("hashed_password", hashed_password).execute()
            return bool(query.data)
        except Exception as e:
            print(f"Error has occured: {e}")
            return False
        
    # logs in a user
    def addSocialMedia(self, user_id, social_media_platform, social_media_username):
        try: 
            new_contacts = self.supabase.table("users").select("contacts").eq("user_id", user_id).execute().data[0]["contacts"] 
            if new_contacts == None:
                new_contacts = {}
            new_contacts[social_media_platform] = social_media_username
            self.supabase.table("users").update({"contacts": new_contacts}).eq("user_id", user_id).execute()
            return True
        except Exception as e:
            print(f"Error has occured: {e}")
            return False
    
    # logs in a user
    def getContacts(self, user_id):
        try: 
            new_contacts = self.supabase.table("users").select("contacts").eq("user_id", user_id).execute().data[0]["contacts"] 
            return new_contacts
        except Exception as e:
            print(f"Error has occured: {e}")
            return None
        
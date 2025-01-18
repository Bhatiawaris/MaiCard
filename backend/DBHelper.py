import os
from supabase import create_client, Client

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
        query = self.supabase.table("profiles").select("contacts, text").eq('profile_id', profile_id).execute()
        return query.data
    
    # get a users profiles
    def getQRs(self, user_id):
        query = self.supabase.table("profiles").select("profile_id").eq('user_id', user_id).execute()
        return query.data

    # gets a users saves
    def getSaves(self, user_id):
        query = self.supabase.table("saves").select("profile_id, date_saved").eq("user_id", user_id).execute()
        return query.data
    
    def saveProfile(self, user_id, profile_id):
        entry = {
            "user_id" : user_id,
            "profile_id" : profile_id,
            
        }
        query = self.supabase.table("saves").insert({ "user_id":user_id, }).eq("user_id", user_id).execute()
        return query.data
        return 0
        
    
db = DBHelper()
print(db.getProfile(1))
from fastapi import FastAPI
from backend.app.core.DBHelper import DBHelper
app = FastAPI()
db = DBHelper()

@app.get("/")
def read_root():
    db.setupDatabase()
    return {"message": "Hello, FastAPI!"}

@app.get("/test")
def read_root():
    return {"message": db.queryUsers()}

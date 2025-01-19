from fastapi import APIRouter

from app.api.routes import login, users, profiles
from app.core.config import settings
from app.api.routes import profiles

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(profiles.router)


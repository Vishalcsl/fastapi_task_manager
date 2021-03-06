from backend.webapps.tasks import route_tasks
from backend.webapps.users import route_users
from backend.webapps.auth import route_login
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(route_tasks.router, prefix="", tags=["tasks-webapp"])
api_router.include_router(route_users.router, prefix="", tags=["users-webapp"])
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])

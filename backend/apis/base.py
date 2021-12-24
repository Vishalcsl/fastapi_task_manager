# import os, sys; 
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from fastapi import APIRouter

from .version1 import route_users
from .version1 import route_tasks
from .version1 import route_login

api_router = APIRouter()
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])

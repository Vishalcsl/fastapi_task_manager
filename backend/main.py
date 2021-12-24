# import os, sys; 
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.core.config import settings
from backend.apis.base import api_router
from backend.db.session import engine
from backend.db.base import Base
from backend.db.models.tasks import Task
from backend.db.models.users import User
from backend.webapps.base import api_router as web_app_router

# print(os.path.dirname(__file__))
# print(os.path.dirname(os.path.realpath(__file__)))

def include_router(app):
    app.include_router(api_router)
    app.include_router(web_app_router)

def configure_static(app):
    app.mount("/backend/static", StaticFiles(directory="backend/static"), name="static")

def create_tables():
    if not engine.dialect.has_table(engine, Task) and not engine.dialect.has_table(engine, User ): 
        Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    create_tables()
    return app


app = start_application()
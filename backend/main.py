# import os, sys; 
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import schema
from backend.core.config import settings
from backend.apis.base import api_router
from backend.db.session import engine
from backend.db.base import Base
from backend.db.models.tasks import Task
from backend.db.models.users import User
from backend.webapps.base import api_router as web_app_router
import sqlalchemy as sa

# print(os.path.dirname(__file__))
# print(os.path.dirname(os.path.realpath(__file__)))
def table_exists(engine,name):
    ins = sa.inspect(engine)
    ret =ins.dialect.has_table(engine.connect(),name)
    print('Table "{}" exists: {}'.format(name, ret))
    return ret

def include_router(app):
    app.include_router(api_router)
    app.include_router(web_app_router)

def configure_static(app):
    app.mount("/backend/static", StaticFiles(directory="backend/static"), name="static")

def create_tables():
    
    if not table_exists(engine=engine, name="task") and not table_exists(engine=engine, name="user"): 
        Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    create_tables()
    return app


app = start_application()
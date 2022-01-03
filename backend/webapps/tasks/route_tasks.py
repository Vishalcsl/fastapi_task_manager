from fastapi import APIRouter
from fastapi import Request,Depends
from fastapi import templating
from fastapi import responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.sql import expression
from sqlalchemy.sql.functions import user
from backend.apis.version1.route_login import get_current_user_from_token
from backend.db.repository.tasks import create_new_task
import os
from backend.schemas.tasks import TaskCreate
from backend.db.repository.tasks import retreive_task
from backend.db.repository.tasks import get_user_tasks
from backend.db.models.users import User
from backend.webapps.tasks.forms import TaskCreateForm
from fastapi.security.utils import get_authorization_scheme_param
from backend.db.repository.tasks import search_task
from typing import Optional


from backend.db.session import get_db

# templates = Jinja2Templates(directory="templates")
print("******************************************")
print(os.path.abspath())
print("******************************************")
templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('templates')))
#coz this route is serving frontend so we do not need to include this in API documentation
router = APIRouter(include_in_schema=False)

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "/general_pages/homepage.html", {"request": request}
    )

@router.get("/dashboard/{username}/")
async def dashboard(request: Request, username: str, db: Session = Depends(get_db), 
current_user: User = Depends(get_current_user_from_token)):
    all_tasks = get_user_tasks(username=username, db=db)
    return templates.TemplateResponse("users/dashboard.html", {"request": request, "tasks": all_tasks, "username": username})


@router.get("/{username}/task/detail/{id}")
def task_detail(id: int, request:Request, db:Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    task = retreive_task(id=id, db=db)
    return templates.TemplateResponse("tasks/detail.html", {"request":request, "task":task})


@router.get("/{username}/create-task")
def create_task(username: str, request: Request, db:Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    return templates.TemplateResponse("tasks/create_task.html", {"request": request})

@router.post("/{username}/create-task")
async def create_task(username: str, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    form = TaskCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )
            current_user = get_current_user_from_token(token=param, db=db)
            task = TaskCreate(**form.__dict__)
            task = create_new_task(task=task, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(f"/{username}/task/detail/{task.id}", status_code=status.HTTP_302_FOUND)

        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "Oops!! some error occured"
            )
            return templates.TemplateResponse("tasks/create_task.html", form.__dict__)
    return templates.TemplateResponse("tasks/create_task.html", form.__dict__)


@router.get("/{username}/delete-task/")
def show_jobs_to_delete(username: str, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    tasks = get_user_tasks(username=username, db=db)
    return templates.TemplateResponse("tasks/show_tasks_to_delete.html", {"request": request, "tasks":tasks})

@router.get("/search/")
def search(request: Request, db: Session = Depends(get_db), 
    query: Optional[str] = None, current_user: User = Depends(get_current_user_from_token)
):
    tasks = search_task(query,db=db)
    return templates.TemplateResponse("users/dashboard.html", {"request": request, "tasks": tasks})
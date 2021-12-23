from os import stat
from fastapi import APIRouter
from pydantic.networks import HttpUrl
from pydantic.utils import deep_update
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from typing import List, Optional

from db.session import get_db
from db.models.tasks import Task
from db.models.users import User
from schemas.tasks import TaskCreate,ShowTask
from db.repository.tasks import create_new_task, retreive_task, get_owner_tasks, update_task_by_id
from db.repository.tasks import delete_task_by_id
from apis.version1.route_login import get_current_user_from_token
from db.repository.tasks import search_task

router = APIRouter()

@router.post("/create-task/", response_model=ShowTask)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    task = create_new_task(task=task, db=db, owner_id=current_user.id)
    return task


@router.get("/get/{id}", response_model=ShowTask)
def read_task(id:int , db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    task = retreive_task(id=id, db=db)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with this id {id} does not exist")
    return task

@router.get("/task-details/{owner_id}", response_model=List[ShowTask])
def read_owner_tasks(owner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    tasks = get_owner_tasks(owner_id=current_user.id, db=db)
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Owner does not have any tasks")
    return tasks

@router.put("/update/{id}")
def update_task(id: int, task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    message = update_task_by_id(id=id, task=task, db=db, owner_id=current_user.id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} not found")
    return {"msg": "Successfully updated data."}


@router.delete("/delete/{id}")
def delete_task(id: int, db:Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    task  = retreive_task(id=id, db=db)
    if not task:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with task id {id} does not exists")
    print(task.owner_id, current_user.id, current_user.is_superuser)
    if task.owner_id == current_user.id or current_user.is_superuser:
        delete_task_by_id(id=id, db=db, owner_id=current_user.id)
        return {"detail": "Successfully deleted."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not permitted!!!")


@router.get("/autocomplete")
def autocomplete(term: Optional[str] = None, db: Session = Depends(get_db)):
    tasks = search_task(term, db=db)
    task_titles = []
    for task in tasks:
        task_titles.append(task.title)
    return task_titles

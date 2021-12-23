from sqlalchemy.orm import Session, session
from db.repository.users import get_user_by_username

from schemas.tasks import TaskCreate
from db.models.tasks import Task

def create_new_task(task: TaskCreate, db: Session, owner_id: int):
    task_object = Task(**task.dict(), owner_id=owner_id)
    db.add(task_object)
    db.commit()
    db.refresh(task_object)
    return task_object

def retreive_task(id:int, db:Session):
    item = db.query(Task).filter(Task.id == id).first()
    return item

def get_owner_tasks(owner_id: int, db:Session):
    items = (db.query(Task).filter(Task.owner_id == owner_id, Task.is_active == True)).all()
    return items

def get_user_tasks(username: str, db:Session):
    user = get_user_by_username(username=username, db=db)
    user_id = user.id
    tasks = get_owner_tasks(owner_id=user_id, db=db)
    return tasks

def update_task_by_id(id: int, task: TaskCreate, db: Session, owner_id: int):
    existing_task = db.query(Task).filter(Task.id == id)
    if not existing_task.first():
        return 0
    task.__dict__.update(owner_id=owner_id)
    existing_task.update(task.__dict__)
    db.commit()
    return 1


def delete_task_by_id(id: int, db: Session, owner_id: int):
    existing_task = db.query(Task).filter(Task.id == id)
    if not existing_task.first():
        return 0
    existing_task.delete(synchronize_session=False)
    db.commit()
    return 1


def search_task(query: str, db: Session):
    tasks =  db.query(Task).filter(Task.title.contains(query))
    return tasks
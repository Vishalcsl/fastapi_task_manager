from typing import Optional
from pydantic import BaseModel
from datetime import date,datetime


class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date_posted: Optional[date] = datetime.now().date()
    completion_by: Optional[date] = datetime.now().date()
    location: Optional[str] = None


# will be used to validate data while creating a task
class  TaskCreate(TaskBase):
    title: str
    location: str
    description: str
    completion_by: date


# this will be used to format the resposne to not have id and owner_id
class ShowTask(TaskBase):
    title: str
    location: str
    date_posted: date
    completion_by: date
    description: Optional[str]
    # to convert dict object to json
    class Config():
        orm_mode = True

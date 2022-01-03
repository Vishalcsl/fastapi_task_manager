import os
from backend.db.repository.users import create_new_user
from backend.db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates
from backend.schemas.users import UserCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.webapps.users.forms import UserCreateForm


# templates = Jinja2Templates(directory="templates")
templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('~/backend/templates')))
router = APIRouter(include_in_schema=False)

@router.get("/register/")
def register(request: Request):
    return templates.TemplateResponse("users/register.html", {"request": request})

@router.post("/register/")
async def register(request: Request, db:Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(
            username = form.username,
            email = form.email,
            firstname = form.firstname,
            lastname = form.lastname,
            password = form.password
        )
        try:
            user = create_new_user(user=user, db=db)
            if not  user:
                form.__dict__.get("errors").append("Email or Username already exists")
                return templates.TemplateResponse("users/register.html", form.__dict__)
            return responses.RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("users/register.html", form.__dict__)
    return templates.TemplateResponse("users/register.html", form.__dict__)
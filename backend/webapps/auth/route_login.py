from fastapi.params import Query
from sqlalchemy.sql.functions import user
from starlette import status
from starlette.responses import RedirectResponse
from backend.apis.version1.route_login import login_for_access_token
from backend.db.repository.users import get_username_by_email
from backend.db.session import get_db
from fastapi import APIRouter, responses
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.webapps.auth.forms import LoginForm

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request, msg:str = None):
    return templates.TemplateResponse("auth/login.html", {"request": request, "msg": msg})


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db), msg:str = Query(None)):
    if msg:
        print(msg)
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            username = get_username_by_email(form.username, db)
            print(username)
            form.__dict__.update(msg="Login Successful :)")
            form.__setattr__("username", username)
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)

@router.get("/logout/")
def logout(request: Request):
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response


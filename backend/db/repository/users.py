from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import or_ 
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import null

from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher


def create_new_user(user:UserCreate, db: Session):
    user_check = db.query(User).filter(or_(User.email == user.email, User.username == user.username)).first()
    print("User Check ", user_check)
    if user_check:
        return null
    
    user = User(username= user.username,
        firstname = user.firstname,
        lastname = user.lastname,
        email = user.email,
        hashed_password = Hasher.get_password_hash(user.password),
        is_active = True,
        is_superuser=False
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(email:str, db:Session):
    user = db.query(User).filter(User.email == email).first()
    return user

def get_user_by_username(username:str, db:Session):
    user = db.query(User).filter(User.username == username).first()
    return user

def get_username_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user.username
from sqlalchemy.orm import Session 
from sqlalchemy.sql.elements import or_
from db.models.users import User

def get_user(username: str, db: Session):
    user = db.query(User).filter(or_(User.email == username, User.username == username)).first()
    return user
from sqlalchemy import Column,Integer, String,Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

from db.base_class import Base


class User(Base):
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,nullable=False)
    firstname= Column(String, nullable=False)
    lastname = Column(String, nullable=True)
    email = Column(String,nullable=False,unique=True,index=True)
    hashed_password = Column(String,nullable=False)
    is_active = Column(Boolean(),default=True)
    is_superuser = Column(Boolean(),default=False)
    tasks = relationship("Task",back_populates="owner")
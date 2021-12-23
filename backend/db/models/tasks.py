from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base

class Task(Base):
    id = Column(Integer, primary_key= True, index=True)
    title=Column(String, nullable=False)
    description= Column(String, nullable=False)
    date_posted= Column(Date)
    completion_by= Column(Date)
    location = Column(String, nullable=True)
    is_active = Column(Boolean(),default=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates='tasks')
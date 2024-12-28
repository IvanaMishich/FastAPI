from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base


class Todo(Base):
    __tablename__ = 'Todo'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
    important = Column(Boolean, default=False)


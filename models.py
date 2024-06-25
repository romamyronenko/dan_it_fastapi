from sqlalchemy import Column, String, Integer

from database import Base


class ToDoList(Base):
    __tablename__ = "todolist"

    id = Column(Integer, primary_key=True)
    name = Column(String)


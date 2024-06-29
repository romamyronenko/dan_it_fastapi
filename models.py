from typing import List

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from database import Base


class ToDoList(Base):
    __tablename__ = "todolist"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    tasks: Mapped[List["Task"]] = relationship()

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_done = Column(Boolean)
    description = Column(String)

    todolist_id: Mapped[int] = mapped_column(ForeignKey('todolist.id'))


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    username = Column(String)
    password = Column(String)

    todolists: Mapped[List["ToDoList"]] = relationship()

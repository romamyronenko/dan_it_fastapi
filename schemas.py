from pydantic import BaseModel


class ToDoList(BaseModel):
    name: str


class Task(BaseModel):
    name: str
    description: str
    is_done: bool


class UpdateTasK(BaseModel):
    name: str = None
    description: str = None
    is_done: bool = None
    todolist_id: int = None

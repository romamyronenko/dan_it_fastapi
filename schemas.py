from pydantic import BaseModel


class ToDoList(BaseModel):
    name: str

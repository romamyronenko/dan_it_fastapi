from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import database
import models
from schemas import ToDoList
from . import list_tasks

router = APIRouter(prefix="/todolists",)
router.include_router(list_tasks.router, prefix="/{list_id}")
@router.post("/")
async def create_todolist(data: ToDoList, db: AsyncSession = Depends(database.get_db)):
    todolist = models.ToDoList(name=data.name)
    db.add(todolist)
    await db.commit()
    await db.refresh(todolist)
    return {'message': 'created', 'id': todolist.id}


@router.get('/')
async def show_all_lists(db: AsyncSession = Depends(database.get_db)):
    query = select(models.ToDoList)
    result = await db.execute(query)
    todolists = result.scalars().all()
    return todolists


@router.delete('/{list_id}')
async def delete_list(list_id: int, db: AsyncSession = Depends(database.get_db)):
    query = select(models.ToDoList).filter(models.ToDoList.id == list_id)

    result = await db.execute(query)
    todolist = result.scalar_one_or_none()
    if todolist is not None:
        await db.delete(todolist)
        await db.commit()
        return {"message": "deleted"}
    return {"message": "not found"}


@router.put('/{list_id}')
async def update_list(list_id: int, data: ToDoList, db: AsyncSession = Depends(database.get_db)):
    query = select(models.ToDoList).filter(models.ToDoList.id == list_id)

    result = await db.execute(query)
    todolist = result.scalar_one_or_none()

    todolist.name = data.name
    if todolist is not None:
        await db.commit()
        await db.refresh(todolist)
        return {"message": "updated", 'todolist': todolist}
    return {"message": "not found"}
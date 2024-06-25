from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import database
import models
import schemas

router = APIRouter(prefix="/tasks", )


@router.post("/")
async def create_task(data: schemas.Task, list_id: int, db: AsyncSession = Depends(database.get_db)):
    print(data.dict())
    task = models.Task(
        todolist_id=list_id,
        **data.dict(),
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return {'message': 'created', 'id': task.id}


@router.get('/')
async def show_all_tasks(list_id: int, db: AsyncSession = Depends(database.get_db)):
    query = select(models.Task).where(models.Task.todolist_id == list_id)
    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks


@router.put('/{task_id}')
async def update_task(data: schemas.UpdateTasK, task_id: int, db: AsyncSession = Depends(database.get_db)):
    query = select(models.Task).filter(models.Task.id == task_id)

    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if data.name:
        task.name = data.name

    if data.description:
        task.description = data.description

    if data.is_done:
        task.is_done = data.is_done

    if data.todolist_id:
        task.todolist_id = data.todolist_id

    if task is not None:
        await db.commit()
        await db.refresh(task)

        return {"message": "updated", "task": task}
    return {"message": "not found"}


@router.delete('/{task_id}')
async def delete_task(task_id: int, db: AsyncSession = Depends(database.get_db)):
    query = select(models.Task).filter(models.Task.id == task_id)

    result = await db.execute(query)
    task = result.scalar_one_or_none()
    if task is not None:
        await db.delete(task)
        await db.commit()
        return {"message": "deleted"}
    return {"message": "not found"}

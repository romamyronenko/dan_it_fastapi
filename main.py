from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import database
import models
from schemas import ToDoList


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/todolists")
async def create_todolist(data: ToDoList, db: AsyncSession = Depends(database.get_db)):
    todolist = models.ToDoList(name=data.name)
    db.add(todolist)
    await db.commit()
    await db.refresh(todolist)
    return {'message': 'created', 'id': todolist.id}


@app.get('/todolists')
async def show_all_lists(db: AsyncSession = Depends(database.get_db)):
    query = select(models.ToDoList)
    result = await db.execute(query)
    todolists = result.scalars().all()
    return todolists


@app.delete('/todolists/{list_id}')
async def delete_list(list_id: int, db: AsyncSession = Depends(database.get_db)):
    query = select(models.ToDoList).filter(models.ToDoList.id == list_id)

    result = await db.execute(query)
    todolist = result.scalar_one_or_none()
    if todolist is not None:
        await db.delete(todolist)
        await db.commit()
        return {"message": "deleted"}
    return {"message": "not found"}


@app.put('/todolists/{list_id}')
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




if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', reload=True)

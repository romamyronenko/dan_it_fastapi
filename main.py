from contextlib import asynccontextmanager

from fastapi import FastAPI

import database
import models
from routes import auth
from routes import todolists


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(todolists.router)
app.include_router(auth.router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', reload=True)

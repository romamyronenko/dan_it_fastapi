import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

MYSQL_USER = os.getenv("MYSQL_USER", 'roma')
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", '123')
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "todo_db")
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql_todolist')
print(MYSQL_HOST)
DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        yield session

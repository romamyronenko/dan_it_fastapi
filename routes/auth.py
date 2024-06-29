import jwt
from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import database
import models
import schemas

SECRET = "asdfewf234f"
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_token(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        username = payload.get("username")
        query = select(models.User).where(models.User.username==username)
        result = await db.execute(query)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid user"
            )
        return payload

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )


@router.post("/token")
async def get_token(user: schemas.User, db: AsyncSession = Depends(database.get_db)):
    query = select(models.User).where(
        models.User.password == user.password and models.User.username == user.username
    )
    result = await db.execute(query)
    if result:
        user_ = result.all()[0][0]
        print(user_.id)
        token_data = {"username": user_.username, "user_id": user_.id}

        token = jwt.encode(token_data, SECRET, algorithm="HS256")

        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong username or password"
    )


@router.post('/register')
async def register(user: schemas.User, db: AsyncSession = Depends(database.get_db)):
    user_ = models.User(**user.dict())
    db.add(user_)
    await db.commit()
    return {'message': 'registered'}
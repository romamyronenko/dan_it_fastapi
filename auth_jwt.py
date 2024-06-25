import jwt
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

SECRET = "asdfewf234f"

DB = {
    'user1': 'password1',
    'user2': 'password2',
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        username = payload.get('username')
        if username not in DB:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid user')
        return username

    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token')


app = FastAPI()


@app.get("/")
def home(user: str = Depends(verify_token)):
    data = {'user': user}
    return data


@app.post("/token")
def get_token(username, password):
    if DB.get(username) == password:
        token_data = {'username': username}

        token = jwt.encode(token_data, SECRET, algorithm='HS256')

        return {'access_token': token, 'token_type': 'bearer'}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='wrong username or password')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('auth_jwt:app')

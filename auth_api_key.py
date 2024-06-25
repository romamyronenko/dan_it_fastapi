from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader

api_keys = {
    '23f23rf23rf': '1',
    'asdnuiq23hd7823': '2'
}

app = FastAPI()

header_key = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_key(api_key_header=Depends(header_key)):
    if api_key_header is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='api key not provided')
    if api_key_header not in api_keys:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid api key')

    return api_key_header


@app.get("/")
def home(api_key: str = Depends(get_api_key)):
    return {'api key': api_key, 'user_id': api_keys[api_key]}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('auth_api_key:app')

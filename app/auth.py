from jose import jwt
from fastapi import HTTPException, Header
from config import SECRET_KEY, ALGORITHM
from passlib.context import CryptContext


def create_token(username:str):
    payload = {
        "sub": username
        }
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token


def verify_token(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=400, detail="le token est invalide")
    


password_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hache_password(password: str):
    return password_context.hash(str(password))

def verify_password(password,hash_password):
    return password_context.verify(password,hash_password)
    
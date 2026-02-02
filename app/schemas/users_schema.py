from pydantic import BaseModel


class UserCreate(BaseModel):
    username : str
    email : str
    password : str


class UserVerify(BaseModel):
    username : str
    password : str

class UserResponse(UserCreate):
    id : int
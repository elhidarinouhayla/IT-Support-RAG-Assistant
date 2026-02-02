from pydantic import BaseModel


class QueryCreate(BaseModel):
    userid : int
    question : str
    answer : str
    cluster : int


class UserResponse(QueryCreate):
    id : int
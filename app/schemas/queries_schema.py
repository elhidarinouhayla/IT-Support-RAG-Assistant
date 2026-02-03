from pydantic import BaseModel


class QueryCreate(BaseModel):
    user_id: int
    question: str
    answer: str
    cluster: int
    latency_ms: float



class QueryInput(BaseModel):
    question: str

class QueryResponse(BaseModel):
    cluster: int
    answer: str
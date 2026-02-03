from pydantic import BaseModel


class QueryCreate(BaseModel):
    user_id: int
    question: str
    answer: str
    cluster: int
    latency_ms: float
    


class QueryResponse(QueryCreate):
    id : int
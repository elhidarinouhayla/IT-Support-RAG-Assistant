from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str



class QueryResponse(BaseModel):
    user_id: int
    question: str
    cluster: int
    answer: str
    latency_ms: float




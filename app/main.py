from fastapi import FastAPI, HTTPException,Depends
from app.database import Base, engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.users_schema import UserCreate, UserResponse, UserVerify
from app.schemas.queries_schema import QueryResponse, QueryRequest
from app.models.users_model import User
from app.models.queries_model import Querie
from .auth import create_token, verify_password, verify_token, hache_password
from .services.kmeans_service import cluster
import time
from utils.embedding import configuration
from utils.embedding import rag_chain





app = FastAPI()
Base.metadata.create_all(bind=engine)




# creation d'un username :
@app.post("/register", response_model=UserResponse)
def create_user(user:UserCreate, db: Session=Depends(get_db)):
    exist = db.query(User).filter(User.username == user.username).first()

    if exist:
        raise HTTPException(status_code=400, detail= "username existe deja")
    
    # haching password
    hashed_pwd = hache_password(user.password)
    
    new_user = User(username=user.username, password=hashed_pwd, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



#  verifier l'identifiant et encoder token
@app.post("/login")
def login(user:UserVerify, db: Session=Depends(get_db)):

    db_user = db.query(User).filter(
        User.username == user.username
        ).first()
    
    if not db_user or not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=400, detail="username or password incorect")
    
    token = create_token(db_user.username, user_id=db_user.id)

    return {"token" : token}



@app.post("/query", response_model=QueryResponse)
def query(querie: QueryRequest, user = Depends(verify_token), db: Session = Depends(get_db)):

    start_time = time.time()

    cluster_label = cluster(querie.question)

    result = rag_chain.invoke({"query": querie.question})

    
    latency_ms = (time.time() - start_time) * 1000

    return QueryResponse(
        user_id=user.get("id", 0),
        question=querie.question,
        cluster=cluster_label,
        answer=result["result"],
        latency_ms=latency_ms
    )    


@app.get("/history")
def history(db: Session = Depends(get_db)):

    queries = db.query(Querie).order_by(Querie.created_at.desc()).all()
    history = []
    
    for q in queries:
        
        history.append({
            "question": q.question,
            "answer": q.answer,
            "cluster": q.cluster,
            "latency_ms": q.latency_ms,
            "created_at": q.created_at
        })
    return {"history": history}



# @app.get("/history")
# def history(db: Session = Depends(get_db), current_user: UserResponse = Depends(verify_token)):

#     queries = db.query(Querie).filter(Querie.user_id == current_user.id).all()
#     if not queries:
#         return {"message": "No queries found for the user."}

#     return {"queries": queries}




@app.get("/health")
def health(db: Session=Depends(get_db)):

    return {"message": "Backend service is healthy"}
from fastapi import FastAPI, HTTPException,Depends
from .database import Base, engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.users_schema import UserCreate, UserResponse, UserVerify
from app.schemas.queries_schema import QueryCreate, QueryResponse, QueryInput
from app.models.users_model import User
from app.models.queries_model import Querie
from .auth import create_token, verify_password, verify_token, hache_password
from utils.embedding import configuration, rag_chain
from .services.kmeans_service import cluster




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
    
    token = create_token(db_user.username)

    return {"token" : token}



@app.post("/query", response_model=QueryResponse)
def query(querie: QueryInput, db: Session=Depends(verify_token)):

    cluster_label = cluster(querie.question)

    result = rag_chain.invoke({"query": querie.question})
    return QueryResponse(cluster=cluster_label, answer=result["result"])
    
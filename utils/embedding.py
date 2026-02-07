from langchain_community.embeddings import HuggingFaceEmbeddings
from .pdf_loading import load_pdf
from .text_splitter import split_pages
from langchain_community.vectorstores import Chroma
import os
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
# from config import GEMINI_API_KEY

from dotenv import load_dotenv
import os
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


pdf_path = "./data/raw/data.pdf"

pages = load_pdf(pdf_path)
chunks = split_pages(pages)


def save_vectordb():

    embedding_model = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )

    texts = [chunk.page_content for chunk in chunks]


    embeddings = embedding_model.embed_documents(texts)


    # Save to a vector db
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory ="../data/vectordb/chroma_db"
    ) 

    return vector_db

vector_db = save_vectordb()

# template du prompt
prompt = """Tu es un assistant IT support expert. 
Réponds UNIQUEMENT à partir du contexte fourni ci-dessous.
Si l'information n'est pas dans le contexte, dis "Je n'ai pas cette information dans la documentation".

Contexte:
{context}

Question: {question}

Réponse (en français, claire et précise):"""

PROMPT = PromptTemplate(
    template=prompt,
    input_variables=["context", "question"]
)


def configuration(vector_db):
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0,
        google_api_key=GEMINI_API_KEY
        )
    
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )
    return rag_chain

rag_chain = configuration(vector_db)

# db = save_vectordb()
# reponse = configuration(db)

# question = "Quelles sont les informations importantes mentionnees dans le document ?"
# answer = reponse.invoke({"query": question})

# print("chatbot response :")
# print(answer["result"])




import mlflow
import time

mlflow.set_tracking_uri("./mlruns")
mlflow.set_experiment("RAG_IT_SUPPORT")

question = "Quelles sont les informations importantes mentionnees dans le document ?"

with mlflow.start_run(run_name="RAG_Gemini_Run"):

    start_time = time.time()

    mlflow.log_param("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")
    mlflow.log_param("llm_model", "gemini-flash-latest")
    mlflow.log_param("vector_db_path", "../data/vectordb/chroma_db")

    vector_db = save_vectordb()
    rag_chain = configuration(vector_db)

    answer = rag_chain.invoke({"query": question})

    latency = (time.time() - start_time) * 1000
    mlflow.log_metric("latency_ms", latency)

    mlflow.log_text(answer["result"], "test_answer.txt")

    print("Réponse MLflow :")
    print(answer["result"])


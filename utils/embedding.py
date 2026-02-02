from langchain.embeddings import HuggingFaceEmbeddings
from .pdf_loading import load_pdf
from .text_splitter import split_pages
from langchain_community.vectorstores import Chroma
import os
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from ..config import GEMINI_API_KEY


pdf_path = "C:/Users/hp/Desktop/IT-Support-RAG-Assistant/data/raw/data.pdf"

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
 



def configuration(vector_db):
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0,
        google_api_key=GEMINI_API_KEY
        )
    
    retr = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3})
    )
    return retr

db = save_vectordb()
reponse = configuration(db)

question = "Quelles sont les informations importantes mentionnees dans le document ?"
answer = reponse.invoke({"query": question})

print("chatbot response :")
print(answer["result"])
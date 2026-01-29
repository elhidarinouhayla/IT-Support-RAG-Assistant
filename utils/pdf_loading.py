from pypdf import PdfReader

from langchain_community.document_loaders import PyPDFLoader



pdf_path = "C:/Users/hp/Desktop/IT-Support-RAG-Assistant/data/raw/data.pdf"

loader = PyPDFLoader(pdf_path)

pages = loader.load()

print(f" PDF charge avec succes")
print(f"   Nombre de pages: {len(pages)}")
print(pages)


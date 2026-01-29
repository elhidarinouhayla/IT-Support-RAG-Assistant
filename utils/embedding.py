from langchain.embeddings import HuggingFaceEmbeddings
from pdf_loading import load_pdf
from text_splitter import split_pages

pdf_path = "C:/Users/hp/Desktop/IT-Support-RAG-Assistant/data/raw/data.pdf"

pages = load_pdf(pdf_path)
chunks = split_pages(pages)


# print(f"Nombre de pages chargées : {len(pages)}")
# print(f"Nombre de chunks : {len(chunks)}")
# print(" chunks:" , chunks[0])


embedding_model = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

texts = [chunk.page_content for chunk in chunks]


embeddings = embedding_model.embed_documents(texts)

print(f"Nombre de textes : {len(texts)}")
print(f"Nombre d'embeddings : {len(embeddings)}")
print(f"Dimension d'un embedding : {len(embeddings[0])}")

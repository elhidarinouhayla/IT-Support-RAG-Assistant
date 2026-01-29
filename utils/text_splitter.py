from langchain.text_splitter import RecursiveCharacterTextSplitter
from pdf_loading import pages



text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,   
    chunk_overlap=50,
    length_function=len
)

chunks = text_splitter.split_documents(pages)

print(f"decoupage termine")
print(chunks)

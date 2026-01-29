from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_pages(pages):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,   
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(pages)
    return chunks

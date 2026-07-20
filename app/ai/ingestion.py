from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


from app.ai.vector_store import get_vector_store

def ingest_pdf(filepath: str) -> int:
    loader = PyPDFLoader(filepath)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = text_splitter.split_documents(pages)

    vector_store = get_vector_store()

    vector_store.add_documents(chunks)

    return len(chunks)
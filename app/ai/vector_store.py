import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

PERSIST_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "refund_policy_docs"

_embeddings_model = None


def get_embeddings_model() -> GoogleGenerativeAIEmbeddings:
    global _embeddings_model
    if _embeddings_model is None:
        _embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    return _embeddings_model

def get_vector_store() -> Chroma:
    return Chroma(
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings_model(),
    )
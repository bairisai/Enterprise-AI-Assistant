# experiments/rag_basics.py
from dotenv import load_dotenv
load_dotenv()

sample_document = """
Our return policy allows customers to return most items within 30 days of purchase for a full refund.
Items must be unused and in their original packaging with all tags attached.

Damaged or defective items can be exchanged within 30 days of purchase, provided the original receipt
is included. Exchanges are not available for sale items or gift cards.

International orders follow a separate return process. Customers must contact our international
support team within 14 days of delivery to initiate a return. Return shipping costs for international
orders are the customer's responsibility unless the item arrived damaged.

Refunds are typically processed within 5-7 business days after we receive the returned item.
Refunds are issued to the original payment method used for the purchase.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap = 120,
)

chunks = text_splitter.split_text(sample_document)

for i, chunk in enumerate(chunks):
    print(f"----Chunk {i} -----")
    print(chunk)
    print()

from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

chunk_embeddings = embeddings_model.embed_documents(chunks)
print(f"Number of chunk embeddings: {len(chunk_embeddings)}")
print(f"Each embedding length: {len(chunk_embeddings[0])}")

question = "What happens if my item arrives damaged from another country?"

question_embedding = embeddings_model.embed_query(question)

import numpy as np

def cosine_similarity(vec_a, vec_b) -> float:
    vec_a = np.array(vec_a)
    vec_b = np.array(vec_b)
    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))

similarities = [cosine_similarity(question_embedding, chunk_vec) for chunk_vec in chunk_embeddings]

for i, score in enumerate(similarities):
    print(f"Chunk {i} similarity: {score:.4f}")

best_index = int(np.argmax(similarities))
print(f"\nMost relevant chunk (index {best_index}, score {similarities[best_index]:.4f}):")
print(chunks[best_index])
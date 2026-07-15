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
    chunk_size=200,
    chunk_overlap=120,
)

chunks = text_splitter.split_text(sample_document)

for i, chunk in enumerate(chunks):
    print(f"----Chunk {i} -----")
    print(chunk)
    print()

from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

question = "What happens if my item arrives damaged from another country?"

from langchain_chroma import Chroma
from langchain_core.documents import Document

documents = [Document(page_content=chunk) for chunk in chunks]

vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings_model,
)

results = vector_store.similarity_search(question, k=2)

for i, doc in enumerate(results):
    print(f"--- Result {i} ---")
    print(doc.page_content)
    print()
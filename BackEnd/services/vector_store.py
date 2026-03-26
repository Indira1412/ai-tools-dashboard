# services/vector_store.py

import chromadb
import uuid

# ---------------- Chroma Client -----------------
# Use PersistentClient to save embeddings to disk
  # your folder
client = chromadb.PersistentClient(path="./chroma_db")
# Name your collection
COLLECTION_NAME = "documents"

# Create or get collection
try:
    collection = client.get_collection(COLLECTION_NAME)
except chromadb.errors.NotFoundError:
    collection = client.create_collection(name=COLLECTION_NAME)

# ---------------- Store embeddings -----------------
def store_embeddings(chunks, embeddings):
    """
    Store chunks + embeddings in Chroma collection.
    """
    ids = [str(uuid.uuid4()) for _ in range(len(chunks))]  # unique IDs to avoid overwrite
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )
    print(f"{len(chunks)} embeddings stored successfully!")

# ---------------- Search documents -----------------
def search_documents(query_embedding, k=3):
    """
    Retrieve top-k similar chunks from Chroma collection.
    """

    # Ensure embedding format is correct
    if isinstance(query_embedding[0], list):
        query_embeddings = query_embedding
    else:
        query_embeddings = [query_embedding]

    results = collection.query(
        query_embeddings=query_embeddings,
        n_results=k
    )

    # Flatten the result
    retrieved = [doc for sublist in results["documents"] for doc in sublist]

    return retrieved
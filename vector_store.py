import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
client = chromadb.PersistentClient(path="./chroma_db")

def create_collection(doc_id: str):
    return client.get_or_create_collection(name=doc_id)

def add_chunks(collection, chunks: list[str]):
    embeddings = model.encode(chunks).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)

def search_similar(collection, query: str, top_k: int = 3) -> list[str]:
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return results["documents"][0]
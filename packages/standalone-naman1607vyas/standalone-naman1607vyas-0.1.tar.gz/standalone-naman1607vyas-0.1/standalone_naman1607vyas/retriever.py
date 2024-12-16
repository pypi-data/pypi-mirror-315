from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def initialize_retriever(documents):
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    document_embeddings = embedding_model.encode(documents)
    document_embeddings = np.array(document_embeddings, dtype=np.float32)
    
    faiss_index = faiss.IndexFlatL2(document_embeddings.shape[1])
    faiss_index.add(document_embeddings)
    return faiss_index, embedding_model
    
def retrieve_context(query, embedding_model, faiss_index, documents, top_k=3):
    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding, dtype=np.float32)
    distances, indices = faiss_index.search(query_embedding, top_k)
    return [documents[i] for i in indices[0]]

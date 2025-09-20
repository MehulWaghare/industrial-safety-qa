import faiss, pickle, numpy as np
from sentence_transformers import SentenceTransformer

INDEX_FILE = "db/faiss.index"
META_FILE = "db/meta.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS and metadata
index = faiss.read_index(INDEX_FILE)
with open(META_FILE, "rb") as f:
    meta = pickle.load(f)

def search(query, k=5):
    q_emb = model.encode([query])
    D, I = index.search(q_emb, k)
    results = []
    for score, idx in zip(D[0], I[0]):
        results.append({
            "score": float(score),
            "text": meta["texts"][idx]
        })
    return results

# Example
if __name__ == "__main__":
    q = "How to safeguard employees from amputations?"
    for r in search(q):
        print(r)

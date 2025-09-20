import sqlite3, faiss, pickle
from sentence_transformers import SentenceTransformer

DB_PATH = "db/chunks.db"
INDEX_FILE = "db/faiss.index"
META_FILE = "db/meta.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load chunks
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("SELECT id, text FROM chunks")
rows = cur.fetchall()
conn.close()

ids, texts = zip(*rows)
embeddings = model.encode(list(texts), convert_to_numpy=True, show_progress_bar=True)

# FAISS index
d = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(embeddings)
faiss.write_index(index, INDEX_FILE)

# Save metadata
with open(META_FILE, "wb") as f:
    pickle.dump({"ids": ids, "texts": texts}, f)

print("✅ Embeddings indexed and saved.")

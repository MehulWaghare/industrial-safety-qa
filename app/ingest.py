import os
import sqlite3
import pdfplumber
import json
from urllib.parse import urlparse, unquote
import sys
import contextlib

# -----------------------------
# Paths
# -----------------------------
PDF_FOLDER = "data/industrial-safety-pdfs"
SOURCES_FILE = "sources_corrected.json"
DB_PATH = "db/chunks.db"

# Ensure db folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# -----------------------------
# Function to chunk text
# -----------------------------
def chunk_text(text, max_len=800):
    words = text.split()
    chunks = []
    cur_chunk = []
    cur_len = 0
    for w in words:
        cur_chunk.append(w)
        cur_len += len(w) + 1
        if cur_len >= max_len:
            chunks.append(" ".join(cur_chunk))
            cur_chunk, cur_len = [], 0
    if cur_chunk:
        chunks.append(" ".join(cur_chunk))
    return chunks

# -----------------------------
# Helper to suppress PDF warnings
# -----------------------------
@contextlib.contextmanager
def suppress_stderr():
    with open(os.devnull, "w") as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr

# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":

    # Create SQLite DB and table
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        text TEXT
    )
    """)
    conn.commit()

    # Load sources JSON
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources = json.load(f)

    # Process each PDF
    for s in sources:
        filename = os.path.basename(unquote(urlparse(s["url"]).path))
        pdf_file = os.path.join(PDF_FOLDER, filename)

        if not os.path.exists(pdf_file):
            print(f"⚠️ Missing PDF: {pdf_file}")
            continue

        print(f"Processing {pdf_file} ...")

        try:
            # Suppress PDF warnings while opening
            with suppress_stderr():
                with pdfplumber.open(pdf_file) as pdf:
                    full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])

            if not full_text.strip():
                print(f"⚠️ No text extracted from: {pdf_file}")
                continue

            for chunk in chunk_text(full_text):
                cur.execute(
                    "INSERT INTO chunks (source, text) VALUES (?, ?)",
                    (s["title"], chunk)
                )

        except Exception as e:
            print(f"⚠️ Error processing {pdf_file}: {e}")

    conn.commit()
    conn.close()
    print("✅ All chunks stored in SQLite.")

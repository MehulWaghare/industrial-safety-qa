# Industrial Safety QA - Mini RAG + Reranker

## Overview
This project implements a **question-answering system** over a small set of industrial and machine safety documents. It starts with a **baseline similarity search** using embeddings and improves results with a **reranker** to prioritize better evidence.

- **CPU only**, no paid APIs.
- Answers are **extractive** and include **citations**.
- Supports **baseline** and **reranker** modes for comparison.

---

## Folder Structure

industrial-safety-qa/
│
├─ app/
│ ├─ api.py # FastAPI server
│ ├─ search.py # Baseline similarity search
│ ├─ rerank.py # Reranker implementation
│ ├─ qa.py # Answer generation
│ ├─ test_api.py # Script to test API
│
├─ data/
│ ├─ sources.json # Metadata for PDFs
│ └─ pdf_chunks.sqlite # SQLite DB for chunked PDFs
│
├─ requirements.txt # Python dependencies
├─ README.md
├─ 8_questions.txt # Assessment questions and results
└─ .gitignore


---

## Setup

1. **Clone the repository:**
```bash
git clone <your-repo-link>
cd industrial-safety-qa


2. **Create a virtual environment (recommended):**
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux / Mac

3.Install dependencies:

pip install -r requirements.txt

4.run the API server:

python app/api.py
The server will start at http://127.0.0.1:5000.


5.Test the API:

python app/test_api.py

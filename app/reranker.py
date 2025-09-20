import sqlite3
from search import search
import re

DB_PATH = "db/chunks.db"

def keyword_score(chunk, query):
    q_terms = query.lower().split()
    chunk_text = chunk.lower()
    score = sum(chunk_text.count(t) for t in q_terms)
    return score / max(len(q_terms), 1)

def hybrid_rerank(query, k=5, alpha=0.6):
    baseline_results = search(query, k*3)  # get top 3x candidates
    scores = []
    max_kws = max(keyword_score(r['text'], query) for r in baseline_results)
    for r in baseline_results:
        vec_score = r['score']
        kw_score = keyword_score(r['text'], query) / max_kws if max_kws else 0
        final = alpha*vec_score + (1-alpha)*kw_score
        scores.append((final, r))
    scores.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in scores[:k]]

# Example
if __name__ == "__main__":
    q = "Safety guidelines for pneumatic machinery"
    for r in hybrid_rerank(q):
        print(r)

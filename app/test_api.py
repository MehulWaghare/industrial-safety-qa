import requests

# Change this URL depending on your server
url = "http://127.0.0.1:5000/ask"

# Example query
data = {
    "q": "OSHA regulations enforcement",
    "k": 5,
    "mode": "hybrid"  # can be "baseline" or "hybrid"
}

response = requests.post(url, json=data)

try:
    result = response.json()
except Exception as e:
    print("Error decoding JSON:", e)
    print("Raw response:", response.text)
    exit()

print(f"\nAnswer: {result.get('answer', 'No answer')}\n")

contexts = result.get("contexts", [])
seen_texts = set()
unique_contexts = []

# Filter unique contexts
for c in contexts:
    text_snip = c.get("text", "")[:150]
    if text_snip not in seen_texts:
        seen_texts.add(text_snip)
        unique_contexts.append(c)

print("Top Contexts (unique):")
for i, c in enumerate(unique_contexts, start=1):
    # Use 'score' or 'final_score' if reranked
    baseline_score = c.get("score", 0)
    rerank_score = c.get("final_score", baseline_score)
    text = c.get("text", "")
    source = c.get("source", "No source")
    
    print(f"{i}. Baseline Score: {baseline_score:.4f}, Rerank Score: {rerank_score:.4f}, Source: {source}")
    print(f"   Text: {text[:200]}...\n")  # show first 200 chars

from flask import Flask, request, jsonify
from reranker import hybrid_rerank

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    q = data.get("q")
    k = data.get("k", 5)
    mode = data.get("mode", "baseline")
    
    if not q:
        return jsonify({"error": "Missing query"}), 400
    
    if mode == "baseline":
        from search import search
        results = search(q, k)
        reranker_used = False
    else:
        results = hybrid_rerank(q, k)
        reranker_used = True
    
    # Simple extractive answer: first sentence of top chunk
    answer = results[0]['text'].split(".")[0] if results else None
    
    return jsonify({
        "answer": answer,
        "contexts": results,
        "reranker_used": reranker_used
    })

if __name__ == "__main__":
    app.run(debug=True)

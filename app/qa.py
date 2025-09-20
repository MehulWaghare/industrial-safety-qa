def generate_answer(contexts, query):
    if not contexts:
        return None
    best = contexts[0]
    text = best["text"]
    # Just extract first 2-3 lines for now (extractive answer)
    snippet = " ".join(text.split()[:60]) + "..."
    return {
        "answer": snippet,
        "contexts": contexts,
        "citation": best["source"]
    }

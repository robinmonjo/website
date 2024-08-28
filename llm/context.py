def context():
    with open("content/llm_context.md", "r", encoding="utf-8") as f:
        context = f.read()
    return context


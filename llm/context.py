def context():
    with open("content/llm_context.md", "r", encoding="utf-8") as f:
        ctx = f.read()
    return ctx
